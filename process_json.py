#!/usr/bin/env python


"""

Everything that gets sent via POST and is a JSOn jobject lands here for 
further processing

"""
import db_add_content as dbac
import json


print("loading process_json.py")

def distribute_actions(jo):
    
    """
    this is the 'entry' function that then distributes work to the next 
    functions
    """
    
    rj = {}
    result = ""
    
    action = jo["action"]
    
    if action == "adVocFromUrl":
          
        text = jo["text"]
        
        dbac.add_one_word(text)
        
#        now test if it arrived
        
        rj['action'] = "adVocFromUrl"
        rj['result'] = "successfully inserted "
        
        result = json.dumps(rj)
        
    return result
        
        
    
    
    
    
