# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd
import numpy as np
import pickle
import os
import spacy
import random
from spacy.lang.en import English
nlp = spacy.load('en_core_web_md')
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import sqlite3
from sqlite3 import Error


#load job data in dataframe and vector 
data = pd.read_csv('./job_process.csv')
path_file = os.path.join('.','vector.pkl')
with open(path_file,'rb') as f:
    vector = pickle.load(f)
  
path_file = os.path.join('.','vectorizer.pkl')
with open(path_file,'rb') as f:
    tfidf = pickle.load(f)
    
    
#Create database and table to register each candidates info
conn = sqlite3.connect('candidates.db')
cur = conn.cursor()  
cur.execute("""CREATE TABLE IF NOT EXISTS info (
                                    id text PRIMARY KEY,
                                    interview text,
                                    questions_count integer,
                                    sim_score real,
                                    sim_id integer ,
                                    name text,
                                    age text,
                                    title text,
                                    mail text
                                );""")
conn.commit()
conn.close()
   
def preprocess(sent):
    doc = nlp(sent)
    doc_process = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
    return doc_process
  
#to get the closest job
def get_closest_job(query, tf_idf, vectorizer):
    #preprocess query
    query_processed = preprocess(query)
    #get the vector
    query_vec = vectorizer.transform([query_processed]).toarray()
    #compute cosine similarity
    simi = cosine_similarity(query_vec,tf_idf).flatten()
    close_ind = simi.argsort()[::-1]
    return (close_ind[0],simi[close_ind[0]]) 
 
class ActionRegistername(Action):

    def name(self) -> Text:
        return "action_register_name"
    
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Connect to database
        try:
           conn = sqlite3.connect('candidates.db')
           cur = conn.cursor()
        except Error as e:
           print(e)
        user_name = tracker.get_slot('name')
        if tracker.get_slot('name') == None:
           user_name = tracker.latest_message.get('text')
        user_id = tracker.sender_id
       #Check if current session(same user) or new session
        cur.execute("""SELECT * from info where id = ?;""",(user_id,))
        result = cur.fetchone()
        if result == None:
           query = """INSERT into info (id, name) VALUES (?, ?);"""
           cur.execute(query,(user_id, user_name))
        else:
           query = """UPDATE info SET name = ? where id = ?;"""
           cur.execute(query,(user_name, user_id))	
        conn.commit()
        conn.close()
        return []
class ActionRegistermail(Action):

    def name(self) -> Text:
        return "action_register_mail"
    
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Connect to database
        try:
           conn = sqlite3.connect('candidates.db')
           cur = conn.cursor()
        except Error as e:
           print(e)
        user_mail = tracker.get_slot('mail')
        if tracker.get_slot('mail') == None:
           user_mail == tracker.latest_message.get('text')
        user_id = tracker.sender_id
       #Check if current session(same user) or new session
        cur.execute("""SELECT * from info where id = ?;""",(user_id,))
        result = cur.fetchone()
        if result == None:
           query = """INSERT into info (id, mail) VALUES (?, ?);"""
           cur.execute(query,(user_id, user_mail ))
        else:
           query = """UPDATE info SET mail = ? where id = ?;"""
           cur.execute(query,(user_mail, user_id))	
        conn.commit()
        conn.close()
        return []

class ActionInfo(Action):

    def name(self) -> Text:
        return "action_job_details"
    
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Connect to dataframe
        job_list = list(data['Title'].unique())
        dispatcher.utter_message(f"Here, our current opportunities:\n {'-'.join(job_list)}")
        dispatcher.utter_message("Are you interested in one of those positions?")
        return []
 
class ActionMain(Action):

    def name(self) -> Text:
        return "action_interview"
    
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Connect to database
        try:
           conn = sqlite3.connect('candidates.db')
           cur = conn.cursor()
        except Error as e:
           print(e) 
        #collecting user info   
        user_input = tracker.latest_message.get('text').lower()
        user_id = tracker.sender_id
        user_age = tracker.get_slot('age')
        user_title = tracker.get_slot('job_title')
        (sim_ind,score) = get_closest_job(user_input, vector, tfidf)
        n = 1
        #Check if current session(same user) or new session
        cur.execute("""SELECT * from info where id = ?;""",(user_id,))
        result = cur.fetchone()
        if result == None:
            query = """INSERT into info (id, interview, questions_count, sim_score, sim_id, age, title) VALUES (?, ?, ?, ?, ?, ?, ?);"""
            cur.execute(query,(user_id, user_input, n, score, sim_ind, user_age, user_title))
        else:
            if result[1] != None:
               user_input += result[1]
            if result[2] != None:
               n += result[2]
            (sim_ind,score) = get_closest_job(user_input, vector, tfidf)
            query = """UPDATE info SET interview = ? , questions_count = ?, sim_score = ?, sim_id = ? where id = ?;"""
            cur.execute(query,(user_input, n, score, int(sim_ind), user_id))
        verdict = 'continue'
        # Build competencies list. The dataframe cell is a string
        add = (data['Software'][int(sim_ind)].strip('],[')).split(',') + (data['Language'][int(sim_ind)].strip('],[')).split(',')
        print(add)
        #check score
        if score < 0.35:
            if n == 1:
                dispatcher.utter_message(f"we still need to know more :{n,score}")
                dispatcher.utter_message(template="utter_background")
            elif n < 3:
                dispatcher.utter_message(f"An other question about your skills :{n,score}")
                dispatcher.utter_message(template="utter_expertize")
            else:
               verdict = 'not ok'
               dispatcher.utter_message(f"{id} Sorry:{score}")
               dispatcher.utter_message(f"{result[5]}, we presently have no offer matching your profile. Once, we get an offer that matches your profile, we will contact you by e-mail")
        elif score < 0.5 and l == 0:
               verdict = 'not ok'
               dispatcher.utter_message(f"{id} Sorry:{score}")
               dispatcher.utter_message(f"{result[5]}, we presently have no offer matching your profile. Once, we get an offer that matches your profile, we will contact you by e-mail")
        elif score < 0.5 and l != 0:
               verdict = 'almost'
               c = random.randint(0,l-1) #choose a random skill
               dispatcher.utter_message(f"{id} Sorry:{score}")
               dispatcher.utter_message(f"How would you rate your {add[c]} skill on a scale of 1(beginner) to 5(expert)?")
               #start an other action..
        else:
               verdict = 'almost'
               c = random.randint(0,l-1)
               dispatcher.utter_message(f"{id} Sorry:{score}")
               dispatcher.utter_message(f"How would you rate your {add[c]} skill on a scale of 1(beginner) to 5(expert)?")
	       #start an other action..
        conn.commit()
        conn.close()
        return [SlotSet('verdict',verdict)]

class ActionBonus(Action):

    def name(self) -> Text:
        return "action_bonus"
    
    def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        #Connect to database
        try:
           conn = sqlite3.connect('candidates_2.db')
           cur = conn.cursor()
        except Error as e:
           print(e) 
        user_id = tracker.sender_id
        rate = int (tracker.latest_message.get('text'))
        cur.execute("""SELECT * from info where id = ?;""",(user_id,))
        result = cur.fetchone()       
        if result != None:
           if rate > 3:
              dispatcher.utter_message(f"Congratulations {result[5]}! We have one offer of {data['Title'].iloc[result[4]]} that pretty match your profile. Find below the application details" )
              dispatcher.utter_message(f"{data['ApplicationP'].iloc[result[4]]} before {data['Deadline'].iloc[result[4]]}")
           else:
             dispatcher.utter_message(f"{result[5]}! you have a good background and your profile may be of interest. HR team may contact you after reviewing")
        conn.commit()
        conn.close()
        return []
    

