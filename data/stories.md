## good_01
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_02
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"not ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_03
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"almost"}
* rate
  - action_bonus
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_04
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_05
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"almost"}
* rate
  - action_bonus
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_06
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"continue"}
* user_profile
  - action_interview
  - slot{"verdict":"not ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_07
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_08
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"almost"}
* rate
  - action_bonus
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_09
* greet
  - utter_greet
  - utter_botdescription
* affirm
  - utter_ask_name
* inform
  - action_register_name
  - utter_ask_mail
* inform
  - action_register_mail
  - utter_userdescription
* user_profile
  - action_interview
  - slot{"verdict":"not ok"}
* thanks OR goodbye OR affirm
  - utter_goodbye

## good_10
* greet
  - utter_greet
  - utter_botdescription
* affirm_search_job_general
  - utter_ask_name

## good_11
* greet
  - utter_greet
  - utter_botdescription
* affirm_search_job_questions
  - action_job_details
* affirm
  - utter_ask_name

## good_12
* greet
  - utter_greet
  - utter_botdescription
* affirm_search_job_questions
  - action_job_details
* deny
  - utter_goodbye

## bad_01
* greet
  - utter_greet
  - utter_botdescription
* deny
  - utter_goodbye

## New Story

* greet
    - utter_greet
    - utter_botdescription
* affirm
    - utter_ask_name
* inform
    - action_register_name
    - utter_ask_mail
* inform
    - action_register_mail
    - utter_userdescription
* user_profile
    - action_interview
    - slot{"verdict":"continue"}
* user_profile
    - action_interview
    - slot{"verdict":"continue"}
* user_profile
    - action_interview
    - slot{"verdict":"not ok"}
* deny
    - utter_goodbye

## Story from conversation with a4af5eb2a45248c1a273bf72c1eeba5a on May 19th 2020

* greet
    - utter_greet
    - utter_botdescription
* affirm
    - utter_ask_name
* inform
    - action_register_name
    - utter_ask_mail
* inform
    - action_register_mail
    - utter_userdescription
* user_profile
    - action_interview
    - slot{"verdict":"almost"}
* rate
    - action_bonus
