#!/usr/bin/env python


from urllib import parse
import json
import process_json as pj
import security
import slave_request
import db_security as dbs
from translate import simple as simple_translate

import log

log.log_info("loading process_post.py")

file_cache = {}

def getFile(path):

    """
    little helper function
    :return:
    """

    global file_cache

    if path in file_cache:
        log.log_info("getFile(path) getting from cache")
        return file_cache[path]

    else:
        log.log_info("getFile(path) loading from file system")
        file = open(path, 'r')
        s = file.read()
        file.close()
        file_cache[path] = s
        return s


def get_translation(json_obj):

    """
    this.language = l;
    this.translationLanguage = tl;
    this.word = w;
    this.translation = "";
    this.action = "translateWord";
    this.session = s;

    :return:
    """

    log.log_info("get_translation(json_obj) = " + str(json_obj))
    lang_from = json_obj["language"]
    lang_to = json_obj["translationLanguage"]
    word = json_obj["word"]

    translation = simple_translate.translate(lang_from, lang_to, word)

    log.log_info("get_translation(json_obj) translation is: " + str(translation))

    return translation



def process_post(form_values, ip_address):

    # this is used by MASTER !!!

    # print("in process_post")
    
    """
    If we have a json object then we convert the string into a json object
    and we continue working with it
    
    """

    log.log_info("process_post(form_values)")
    
    res = ""
    
    if "objJSON" in form_values:

        s = form_values["objJSON"]
        x = s
        j = parse.unquote(x)
        data = json.loads(j)

        res_obj = None

        ip = ""
        port = -1

        # we need to know to which salve server to route the request
        if "session" in data:
            session = data["session"]
            log.log_info("session=" + str(session))
            ip, port = security.get_slave_ip_port_from_session(session.strip())

            # if the session cannot be linked to a user then we need to send user back to login because we don't know where
            # to route

            if port == -1:

                log.log_info("action=" + str(data["action"]))
                log.log_info("port is -1")

                if data["action"] == "logIn":
                    # this means we know the user and should get
                    # get user id from email address
                    #id = dbs.get_user_id(data["user"])
                    ip, port = security.get_slave_ip_port(data["user"])

                    if port == -1:
                        log.log_error("this user is unknown: " + str(data["user"]))

                    #dbs.get_slave_id_from_session_or_user(data["user"])

                if data["action"] == "registerUser":
                    # we might already know this user and therefore better if we first check
                    # get_slave_ip_port(user_id)
                    ip, port = dbs.get_slave_ip_port(data["user"].strip())

                    if port < 0:
                        # this means we don't know the user and forward to a random server
                        ip, port = dbs.get_random_slave_ip_port()
                    else:
                        ip, port = security.get_slave_ip_port(data["user"].strip())

                    log.log_info("with session registerUser = using ip: " + ip)
                    log.log_info("with session registerUser = using port: " + str(port))
                    res_obj = slave_request.get_from_slave(ip, port, data)
                    log.log_info("answer from slave received " + str(res_obj))

                if data["action"] == "checkSession":
                    session = data["session"]
                    ip, port = security.get_slave_ip_port_from_session(session.strip())

                    if port == -1:
                        log.log_info("invalid session. Master sends back to client immediately without forwarding to slave")
                        res_obj = data
                        log.log_info("invalid session " + session)
                        res_obj['sessionValid'] = False

                elif data["action"] == "resetPassword":

                    ip, port = security.get_slave_ip_port(data["user"])

                    if int(port) > 0:
                        log.log_info(("sending data to slave"))
                        res_obj = slave_request.get_from_slave(ip, port, data)
                        log.log_info(("answer from slave received"))
                    else:
                        log.log_error("port is not larger than 0")
                        # Todo: proper error handling
                        res_obj = data

            if int(port) > 0:

                # translateWord
                if data["action"] == "translateWord":
                    log.log_info("now translating a word")
                    res_obj = data
                    res_obj["translation"] = get_translation(data)

                else:
                    log.log_info(("sending data to slave"))
                    res_obj = slave_request.get_from_slave(ip, port, data)
                    log.log_info(("answer from slave received"))
            else:
                log.log_error("port is not larger than 0")
        else:
            # it is possible that login comes without a session
            if data["action"] == "logIn":

                ip, port = security.get_slave_ip_port(data["user"])

                if port == -1:
                    log.log_error("this user is unknown: " + str(data["user"]))

                if int(port) > 0:
                    log.log_info(("sending data to slave"))
                    res_obj = slave_request.get_from_slave(ip, port, data)
                    log.log_info(("answer from slave received"))
                else:
                    log.log_error("port is not larger than 0")
                    # Todo: proper error handling
                    res_obj = data

            elif data["action"] == "resetPassword":

                ip, port = security.get_slave_ip_port(data["user"])

                if int(port) > 0:
                    log.log_info(("sending data to slave"))
                    res_obj = slave_request.get_from_slave(ip, port, data)
                    log.log_info(("answer from slave received"))
                else:
                    log.log_error("port is not larger than 0")
                    # Todo: proper error handling
                    res_obj = data

            elif data["action"] == "registerUser":
                # we might already know this user and therefore better if we first check
                # get_slave_ip_port(user_id)
                ip, port = dbs.get_slave_ip_port(data["user"].strip())

                if port < 0:
                    # this means we don't know the user and forward to a random server
                    ip, port = dbs.get_random_slave_ip_port()
                else:
                    ip, port = security.get_slave_ip_port(data["user"].strip())

                log.log_info("no session registerUser = using ip: " + ip)
                log.log_info("no session registerUser = using port: " + str(port))
                res_obj = slave_request.get_from_slave(ip, port, data)
                log.log_info("answer from slave received " + str(res_obj))

            elif data["action"] == "translateRss":
                log.log_info("now translating a word in translateRss")
                res_obj = data
                res_obj["translation"] = get_translation(data)

            else:
                # if there is no session element, then maybe we want to stream other things
                # these can only be static content
                #todo: this is not finished yet - need to differentiate between the various kinds of content and add real content
                log.log_info("action=" + str(data["action"]))
                res_obj = data
                res_obj['content'] = getFile("./html/" + str(data["action"]) + ".txt")


        #res = pj.distribute_actions(data)

        # the return value needs to be a string already


        if res_obj is None:

            log.log_error("res_obj is NONE in process post process_post(form_values, ip_address) - input data was: " + str(form_values))
            res_obj = {}

        res = json.dumps(res_obj)

    else:
        """
        this is not implemented yet
        """

        log.log_error("process_post(header_values, form_values): - the form_values is not objJSON")

    return res 
    