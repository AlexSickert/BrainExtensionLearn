
import urllib.request as req
import json
import os
import smtplib

import json
import time
from datetime import datetime

# sleep 30 seconds to prevent conflict with same process in master
#time.sleep(30)


config_params = json.load(open('./config.json'))


url = config_params["url"]
err_master = False
err_slave = False
test_time = str(datetime.now())
err_text = test_time

time_out = float(config_params["timeout"])

a_user = config_params["username"]
a_pass = config_params["password"]

e_user = config_params["mail_user"]
e_pass = config_params["mail_password"]

slave_id = config_params["slave_id"]


def send_mail(to_email, email_subject, email_message):

    global e_pass
    global e_user


    FROM = e_user
    TO = [to_email]

    password = e_pass

    SUBJECT = "" + email_subject

    TEXT = email_message

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # SMTP_SSL Example
    # server_ssl = smtplib.SMTP_SSL(host="smtp.alexandersickert.com", port=465)
    server_ssl = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)


    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(FROM, password)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(FROM, TO, message)
    # server_ssl.quit()
    server_ssl.close()
    print( 'successfully sent the mail')


try:
    resp = req.urlopen(url, timeout=time_out).read()
    # print(resp)
    print("OK, server can be reached")
    err_text += "\r\nOK, server can be reached"
except:
    print("Timeout occured. Server cannot be reached.")
    err_master = True
    err_text += "\r\nTimeout occured. Server cannot be reached."

# -------------------------------------------------------------------------------------

if not err_master:

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
        print(err_text)
    except:
        print("Something went wrong during login.")
        err_slave = True
        err_text += "\r\nSomething went wrong during login."


if err_slave:
    # first we send a mail
    print("sending mail...")
    send_mail("alex.solensky@gmail.com", "BrainVok SLAVE " + slave_id + " Problem [" + test_time + "]", err_text)
    #then we restart the server

    print("restarting server...")
    #os.system("sudo bash /home/restart.sh")
    os.system("sudo bash /home/BrainExtension/restart_slave.sh")
    print("restarting server done.")

