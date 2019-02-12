"""

Collection of functions to verify session and logins


"""

import db_security as dbs
import config as cfg
import log

cache_user_ip_port = {}
cache_session_ip_port = {}

def check_login(user, password):

    ret = dbs.check_login(user, password)

    if ret > 0:
        return True
    else:
        return False


def get_user_id(user):

    return dbs.get_user_id(user)


def get_slave_ip_port(user):

    global cache_user_ip_port

    if user in cache_user_ip_port:
        log.log_info("user from cache: " + str(user))
        ip = cache_user_ip_port[user]["ip"]
        port = cache_user_ip_port[user]["port"]

    else:
        log.log_info("user not in cache yet: " + str(user))
        ip, port = dbs.get_slave_ip_port(user)
        cache_user_ip_port[user] = {}
        cache_user_ip_port[user]["ip"] = ip
        cache_user_ip_port[user]["port"] = port

    log.log_info("user " + str(user) + " has ip and port: " + str(ip) + "/" + str(port))
    return ip, int(port)


def get_slave_ip_port_from_session(session):

    global cache_session_ip_port

    if session in cache_session_ip_port:
        ip = cache_session_ip_port[session]["ip"]
        port = cache_session_ip_port[session]["port"]
    else:
        #user_id = dbs.get_user_id_from_session(session)

        #user_id, slave_id = dbs.get_user_and_slave_id_from_session(session)

        slave_id = dbs.get_slave_id_from_session_or_user(session)

        if len(str(slave_id)) > 0:
            ip = cfg.slaves[slave_id][0]
            port = cfg.slaves[slave_id][1]
        else:
            ip = ""
            port = -1

        #ip, port = dbs.get_slave_ip_port(user_id)

        cache_session_ip_port[session] = {}
        cache_session_ip_port[session]["ip"] = ip
        cache_session_ip_port[session]["port"] = port

    return ip, int(port)


