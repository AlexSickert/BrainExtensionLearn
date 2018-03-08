#!/usr/bin/env python


from urllib import parse
import json
import process_json as pj
import log

log.log_info("loading process_post.py")

def process_post(header_values, form_values):
    
    """
    If we have a json object then we convert the string into a json object
    and we continue working with it
    
    """
    
    res = ""
    
    if "objJSON" in form_values:
        s = form_values["objJSON"]
#        print("json object") 
        x = s.decode('utf-8')
        j = parse.unquote(x)
        # j = j[8:]
        data = json.loads(j)  
        
        print(j)
        res = pj.distribute_actions(data)
        
    else:
        """
        this is not implemented yet
        """
        print("sadfasdfasdfasdfasdf")
        print(s[0:8])
        
        
        
    return res 
    