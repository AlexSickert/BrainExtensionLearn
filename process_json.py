#!/usr/bin/env python


"""

Everything that gets sent via POST and is a JSOn jobject lands here for 
further processing

"""
import db_add_content as dbac
import json
import log
import security as sec
import time


print("loading process_json.py")


def process_json(fragments, json_string):

    log.log_info("in function process_json")

    jo = json.loads(json_string)

    # print(jo)

    ret = {}

    #first check security

    if sec.check_login(jo["user"], jo["password"]):

        user_id = sec.get_user_id(jo["user"])


        if jo["function"] == 'upload_google_spreadsheet':
            log.log_info("received data from Google Spreadsheet")

            # add the word to the dictionary
            language = jo["language"]
            language_translation = "german"
            list_obj = jo["list"]

            dbac.add_spreadsheet_list(user_id, language, language_translation, list_obj)

            ret["function"] = jo["function"]
            ret["error"] = False
            ret["error_description"] = ""

    else:
        ret["error"] = True

    result = json.dumps(ret)

    return result


def distribute_actions(jo):
    
    """
    this is the 'entry' function that then distributes work to the subsequent
    functions
    """

    # check if valid session

    # check login

    log.log_info("in distribute_actions")

    rj = {}
    result = ""
    
    action = jo["action"]

    if action == "addOneWord":

        session = jo["session"]

    elif action == "addText":

        text = jo["text"]
        language = jo["language"]   # the input language

    elif action == "adVocFromUrl":

        log.log_info("in distribute_actions adVocFromUrl")

        user_id = 1

        dbac.add_one_word_txt(user_id, jo["language"], jo["word"], jo["translationLanguage"], jo["translationWord"])

#        now test if it arrived
        log.log_info("in distribute_actions preparing response")
        
        rj['action'] = "adVocFromUrl"
        rj['result'] = "successfully inserted "
        
        result = json.dumps(rj)

    elif action == "loadWord":

        log.log_info("loading new word")

        wordId = jo["wordId"]
        answer = jo["answer"]

        # log.log_info("answer was " + answer)

        rj['action'] = action
        rj["wordId"] = "9999"

        rj["language1"] = "English"
        rj["word1"] = "car"
        rj["language2"] = "German" +  str(time.time())
        rj["word2"] = "Auto"
        rj['error'] = False
        rj['error_description'] = ""

        result = json.dumps(rj)

        print(result)

    elif action == "login":

        # loging and create session

        email = jo["email"]
        password = jo["password"]

    elif action == "logout":

        # logfiles out by destroying session and or cookie?

        session = jo["session"]

    elif action == "reset":

        # reset password and send new passwrod to user by email

        session = jo["session"]

    else:
        # then we have a problem because we do not know the request and we need to throw an error
        log.log_error("unknown method for processing JSON")
        xxx = 111

    return result
        
        
    
    
    
    
