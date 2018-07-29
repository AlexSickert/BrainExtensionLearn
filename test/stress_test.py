




import urllib.request as req
import json
import os
import smtplib

import json
import time
from datetime import datetime
import random


import sys

if len(sys.argv) < 2:
    user_id = str(1)
else:
    user_id = str(int(sys.argv[1]))
    print("Running code for user: " + user_id)

config_params = json.load(open('./stress_test.config.json'))



url = config_params["url"]
err = False
test_time = str(datetime.now())
err_text = test_time

time_out = 10

a_user = config_params["username" + user_id]
a_pass = config_params["password" + user_id]


try:
    resp = req.urlopen(url, timeout=time_out).read()
    print(a_user + " OK, server can be reached")
    err_text += "\r\nOK, server can be reached"
except:
    print(a_user + " Timeout occured. Server cannot be reached.")
    err = True
    err_text += "\r\nTimeout occured. Server cannot be reached."

# ----------------------------------------------------------------------------------------------------------------------

try:

    dj = {}
    dj["user"] = a_user
    dj["password"] = a_pass
    dj["action"] = "logIn"

    d="objJSON=" + json.dumps(dj)

    dby = d.encode("utf-8")

    resp = req.urlopen(url, data=dby, timeout=time_out).read()
    jt = resp.decode()
    jo = json.loads(jt)

    session = jo["session"]
    print(jo)

    err_text += "\r\nOK, Login is possible."
    print(a_user + " OK, Login is possible.")

except:
    print(a_user + " Something went wrong during login.")
    err = True
    err_text += "\r\nSomething went wrong during login."


#get word

print(a_user + " Loading the initial word.")

dj = {}
dj["session"] = session
dj["action"] = "loadWord"
dj["answer"] = ""
dj["wordId"] = ""

d="objJSON=" + json.dumps(dj)

dby = d.encode("utf-8")

resp = req.urlopen(url, data=dby, timeout=time_out).read()
jt = resp.decode()
jo = json.loads(jt)

print(jo)

word_id = jo["wordId"]
counter = 0

while True:

    counter += 1
    start_time = time.time()

    #print("In loop.")

    answer = bool(random.getrandbits(1))

    if answer:
        answer_txt = "YES"
    else:
        answer_txt = "No"

    #print("Answer is:" + answer_txt)


    dj = {}
    dj["session"] = session
    dj["action"] = "loadWord"
    dj["answer"] = answer_txt
    dj["wordId"] = word_id

    d = "objJSON=" + json.dumps(dj)

    dby = d.encode("utf-8")

    resp = req.urlopen(url, data=dby, timeout=time_out).read()
    jt = resp.decode()
    jo = json.loads(jt)

    word_id = jo["wordId"]

    print(a_user + " loop number: ", counter)
    #print("word_id is:" + str(word_id))

    #time.sleep(1)

    end_time = time.time()

    diff = end_time - start_time

    print(a_user + " execution took:", diff)











