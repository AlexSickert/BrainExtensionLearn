#!/usr/bin/env python

"""

this file provides the static files and includes etc. 


"""

print("loading get_includes.py")

def get_include_file_content(p):
    
     
    if p == "/":
        f = './html/index.html'
    if "/include/Controller.js" in p:
        f = './js/Controller.js'
    if p == "/app":
        f = './html/app.html'
    if p == "/include/DataAccess.js":
        f = './js/DataAccess.js'
        
    if p == "/include/UxUi.js":
        f = './js/UxUi.js'
   
    file = open(f, 'rb') 
    s = file.read()   
    file.close()
    return s

