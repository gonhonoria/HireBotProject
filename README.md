### Readme

**Project for a pre-screening bot who will gather user profile and find out whether there is an availbale offer that fit the user profile.**

The bot has been built with Rasa. Rasa is an open source machine learning framework to automate text-and voice-based conversations. 


The project contains the following files

actions.py: code for your custom actions that bot will implement according to user entries

config.yml: configuration of NLU and Core models(Text Processing)

credentials.yml: details for connecting to other services

data/nlu.md: NLU training data with user intents

data/stories.md: the interview stories like a screenplay

domain.yml: the bot assistant’s domain with NLU training and bot responses details

endpoints.yml: details for connecting to channels like fb messenger

models/<timestamp>.tar.giz: trained  models


## To test it locally
pip install rasa
rasa train
rasa runactions & rasa shell

You can also use Rasa X to test it: 
http://35.195.169.83/login
mot de passe: rasa

