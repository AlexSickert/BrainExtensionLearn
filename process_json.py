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
import db_learn as dbl
import db_report as dbr
import db_security as dbs
import db_add_content as dbc
import email_sender
import os
import settings
import slave_request
import urllib.request
import config as cfg
import http.client
import ssl

print("loading process_json.py")


def process_json_master(json_string):
    """

    This is used by the Google Spreadsheet upload

    The master server needs to know to which slave to forward the message. We need to look up the server

    :param json_string:
    :return:
    """

    jo = json.loads(json_string)

    user_id = sec.get_user_id(jo["user"]) # this is the email address

    ip, port = sec.get_slave_ip_port(user_id)

    if port > 0:
        ret_obj = slave_request.get_from_slave(ip, port, jo)

    else:
        # wrong login coordinates
        ret_obj = {}
        ret_obj["error"] = True
        ret_obj["function"] = jo["function"]
        ret_obj["error_description"] = "could not find user"

    return ret_obj


def process_json(json_obj):

    """
    This function is used by the SLAVE ONLY !!!

    This function is currently being used by teh GOOGLE SPREADSHEET upload

    :param fragments:
    :param json_string:
    :return:
    """

    jo = json_obj

    # print(jo)

    ret = {}

    #first check security

    if sec.check_login(jo["user"], jo["password"]):

        log.log_info("login successful for user " + jo["user"])

        user_id = sec.get_user_id(jo["user"])

        if jo["function"] == 'upload_google_spreadsheet':
            log.log_info("received data from Google Spreadsheet")

            # add the word to the dictionary
            language = jo["language"]
            language_translation = jo["mother_tongue"]
            list_obj = jo["list"]

            dbac.add_spreadsheet_list(user_id, language, language_translation, list_obj)

            ret["function"] = jo["function"]
            ret["error"] = False
            ret["error_description"] = ""

    else:
        log.log_info("login failed for user " + jo["user"])
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

        session = jo["session"]
        user_id = dbs.get_user_id_from_session(session)

        time_stamp = int(time.time())

        dbac.add_one_word_txt(user_id, jo["language"], jo["word"], jo["translationLanguage"], jo["translationWord"], True, "", "", time_stamp)
        dbac.add_one_word_txt(user_id, jo["translationLanguage"], jo["translationWord"], jo["language"], jo["word"],  False, "", "", time_stamp)

#        now test if it arrived
        log.log_info("in distribute_actions preparing response")
        
        rj['action'] = "adVocFromUrl"
        rj['result'] = "successfully inserted "
        
        result = json.dumps(rj)

    elif action == "loadWord":

        log.log_info("loading new word")
        log.log_info(jo)

        wordId = jo["wordId"]
        answer = jo["answer"]
        session = jo["session"]

        log.log_info("answer was " + answer)
        log.log_info("wordId was " + str(wordId))
        log.log_info("session was " + str(session))

        user_id = dbs.get_user_id_from_session(session)

        log.log_info("user_id is " + str(user_id))


        success, experiment, once_learned = dbl.process_answer(str(wordId), user_id, answer)

        log.log_info("process_answer done")

        new_id = dbl.get_next_word_id(user_id, str(wordId))

        log.log_info("get_next_word_id done")

        id, l1, w1, l2, w2 = dbl.get_word(new_id)

        rj['action'] = action
        rj["wordId"] = id
        rj["language1"] = dbac.get_language_label(l1)
        rj["word1"] = w1
        rj["language2"] = dbac.get_language_label(l2)
        rj["word2"] = w2
        rj['error'] = False
        rj['error_description'] = ""
        rj['success'] = success
        rj['experiment'] = experiment
        rj['once_learned'] = once_learned

        result = json.dumps(rj)

        log.log_info("distribute_actions(jo) result for new word " + result)

    elif action == "loadWordArray":

        log.log_info("loading new word array")
        log.log_info(jo)

        wordId = jo["wordId"]
        answer = jo["answer"]
        session = jo["session"]

        log.log_info("answer was " + answer)
        log.log_info("wordId was " + str(wordId))
        log.log_info("session was " + str(session))

        user_id = dbs.get_user_id_from_session(session)

        log.log_info("user_id is " + str(user_id))

        # January 2019 we change this logic now using a ordered lost avoiding random
        #success, experiment, once_learned = dbl.process_answer(str(wordId), user_id, answer)
        success, experiment, once_learned = dbl.process_answer_ordered(str(wordId), user_id, answer)

        log.log_info("was experiment? " + str(experiment))
        log.log_info("was success? " + str(success))
        log.log_info("once learned? " + str(once_learned))
        log.log_info("process_answer done")

        # January 2019 trying out a new algorithm using a logic that does not use random, but ordered by logic
        #new_id_array = dbl.get_next_word_id_array(user_id, str(wordId))

        new_id_array = dbl.get_next_word_id_array_ordered_position(user_id, str(wordId))

        word_arr = []

        for new_id in new_id_array:

            row_j = {}
            id, l1, w1, l2, w2 = dbl.get_word(new_id[0])
            row_j["wordId"] = id
            row_j["language1"] = dbac.get_language_label(l1)
            row_j["word1"] = w1
            row_j["language2"] = dbac.get_language_label(l2)
            row_j["word2"] = w2
            row_j["position"] = new_id[1]

            word_arr.append(row_j)

        rj['action'] = action
        rj['error'] = False
        rj['error_description'] = ""
        rj['success'] = success
        rj['experiment'] = experiment
        rj['once_learned'] = once_learned
        rj["words"] = word_arr

        result = json.dumps(rj)

        log.log_info("distribute_actions(jo) result for new word " + result)

    elif action == "editWord":

        session = jo["session"]
        log.log_info("session was " + str(session))
        user_id = dbs.get_user_id_from_session(session)

        fromWord = jo["fromWord"]
        toWord = jo["toWord"]
        word_id = jo["wordId"]

        dbc.update_word_by_id(user_id, fromWord, toWord, word_id)

        log.log_info("update word done")

        rj['action'] = action
        rj['error'] = False
        rj['error_description'] = ""

        result = json.dumps(rj)

    elif action == "report":

        session = jo["session"]
        log.log_info("session was " + str(session))
        user_id = dbs.get_user_id_from_session(session)

        new_words, learned_words = dbr.get_simple_report(user_id)

        html = "<table>"
        html += "<tr>"
        html += "<td>"
        html += "new words:"
        html += "</td>"
        html += "<td>"
        html += str(new_words)
        html += "</td>"
        html += "</tr>"
        html += "<tr>"
        html += "<td>"
        html += "learned words:"
        html += "</td>"
        html += "<td>"
        html += str(learned_words)
        html += "</td>"
        html += "</tr>"
        html += "</table>"

        rj['action'] = action
        rj['newWords'] = new_words
        rj['learnedWords'] = learned_words
        rj['html'] = html
        rj['error'] = False
        rj['error_description'] = ""

        result = json.dumps(rj)

        log.log_info("distribute_actions(jo) result for report " + result)

    elif action == "logIn":

        # login and create session
        user = jo["user"].strip()
        password = jo["password"].strip()
        rj['action'] = "logIn"

        password = password.strip()
        password = password.replace(" ", "")

        user = user.lower()
        user = user.strip()
        user = user.replace(" ", "")

        if dbs.check_login(user, password) > 0:
            rj['success'] = True
            rj['result'] = "success"
            rj['session'] = dbs.make_save_session(user)

            # we need to register the session in the MASTER's database
            register_user_and_session_at_master(rj['session'], user)


        else:
            rj['success'] = False
            rj['result'] = "failure"
            rj['session'] = ""

        log.log_info("result - " + str(rj))
        result = json.dumps(rj)

    elif action == "logout":

        # ToDo
        # logfiles out by destroying session and or cookie?

        session = jo["session"]

    elif action == "checkSession":

        # check if session is valid
        session = jo["session"]
        rj['action'] = "checkSession"

        if dbs.check_session(session) > 0:
            log.log_info("valid session " + session)
            rj['sessionValid'] = True
        else:
            log.log_info("invalid session " + session)
            rj['sessionValid'] = False

        result = json.dumps(rj)

    elif action == "getLanguages":

        rj['action'] = action

        rj['labels'] = ["English", "German", "Russian", "Franch", "Italian", "Spanish", "Portuguese"]
        rj['values'] = ["english", "german", "russian", "franch", "italian", "spanish", "portuguese"]

        rj['error'] = False
        rj['error_description'] = ""

        result = json.dumps(rj)

    elif action == "resetPassword":

        rj['action'] = action

        # ToDo
        # reset password and send new password to user by email

        user = jo["user"]
        user = user.lower()
        user = user.strip()
        user = user.replace(" ", "")

        if dbs.check_user(user) > 0:
            p = dbs.random_string_simple(6)
            dbs.update_password(user, p)
            # ToDo: put in a separate thread to prevent slow down of process
            # ToDo: make nice test in mail
            email_sender.send_mail(user, "resetPassword", "Password: " + p)
            rj['result'] = "success"
            rj['success'] = True
            log.log_info("success in resetting password for " + user)
        else:
            rj['result'] = "failure"
            rj['success'] = False
            log.log_info("failure in resetting password because user not existing " + user)

        result = json.dumps(rj)

    elif action == "registerUser":

        rj['action'] = action

        # ToDo
        # reset password and send new password to user by email

        user = jo["user"]
        user = user.lower()
        user = user.strip()
        user = user.replace(" ", "")

        if dbs.check_user(user) < 1:

            p = dbs.random_string_simple(4)
            dbs.register_user(user, p)

            # ToDo: put in a separate thread to prevent slow down of process
            # ToDo: make nice test in mail
            email_sender.send_mail(user, "registerUser", "password: " + p)

            # wwe need to inform the MASTER about the registration.
            register_user_and_session_at_master("", user)

            log.log_info("registering user " + user)

            rj['result'] = "success"
            rj['success'] = True
        else:

            log.log_info("user already exists: " + user)

            rj['result'] = "failure"
            rj['success'] = False

        result = json.dumps(rj)

    elif action == "getSettings":

        session = jo["session"]

        rj['action'] = action
        rj['settings'] = settings.get_settings(session)
        rj['result'] = "success"
        rj['success'] = True

        result = json.dumps(rj)

    elif action == "setSettings":

        session = jo["session"]

        data = jo["settings"]
        settings.set_settings(session, data)

        rj['action'] = action
        rj['result'] = "success"
        rj['success'] = True

        result = json.dumps(rj)

    else:
        # then we have a problem because we do not know the request and we need to throw an error
        log.log_error("unknown method for processing JSON")
        xxx = 111

    return result
        

def register_user_and_session_at_master(session, user):

    # this is so that the master knows where to forward the request
    # cfg.slave_id
    # url = cfg.parameters["master-url"] + ":" + cfg.parameters["https"] + "/register-slave?security-key=YI64QZ8LMPJET0GV4CCV&"
    # url += "register-session=" + session
    # url += "&server=" + cfg.slave_id
    # url += "&register-user=" + user
    # log.log_info("calling MASTER via URL " + url)
    # r = urllib.request.urlopen(url)
    # log.log_info("MASTER responds " + str(r.read()))


    conn = http.client.HTTPSConnection(cfg.parameters["master-url"], cfg.parameters["https"], context = ssl._create_unverified_context())

    query = "/register-slave?security-key=YI64QZ8LMPJET0GV4CCV&"
    query += "register-session=" + session
    query += "&slave-id=" + cfg.slave_id
    query += "&register-user=" + user

    conn.putrequest('GET', query)
    conn.endheaders()  # <---
    r = conn.getresponse()
    #print(r.read())
    log.log_info("MASTER responds " + str(r.read()))
    
