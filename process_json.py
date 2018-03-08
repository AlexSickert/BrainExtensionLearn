#!/usr/bin/env python


"""

Everything that gets sent via POST and is a JSOn jobject lands here for 
further processing

"""
import db_add_content as dbac
import json
import log


print("loading process_json.py")

def distribute_actions(jo):
    
    """
    this is the 'entry' function that then distributes work to the subsequent
    functions
    """

    # check if valid session

    # check login



    
    rj = {}
    result = ""
    
    action = jo["action"]

    if action == "addOneWord":

        session = jo["session"]

    elif action == "addText":

        text = jo["text"]
        language = jo["language"]   # the input language

    elif action == "adVocFromUrl":
          
        text = jo["text"]
        
        dbac.add_one_word(text)
        
#        now test if it arrived
        
        rj['action'] = "adVocFromUrl"
        rj['result'] = "successfully inserted "
        
        result = json.dumps(rj)

    elif action == "login":

        # loging and create session

        email = jo["email"]
        password = jo["password"]

    elif action == "logout":

        # log out by destroying session and or cookie?

        session = jo["session"]

    elif action == "reset":

        # reset password and send new passwrod to user by email

        session = jo["session"]

    else:
        # then we have a problem because we do not know the request and we need to throw an error
        log.log_error("unknown method for processing JSON")
        xxx = 111

    return result
        
        
    
    
    
    
