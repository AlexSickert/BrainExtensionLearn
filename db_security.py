#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random
import hashlib

#
# conn = dba.get_connection()
# cur = conn.cursor()
# cur.execute("SELECT email, password  FROM users  ", ())
# ret = cur.fetchall()
#
# for row in ret:
#     print("--------------------------")
#     print("email: ", row[0])
#     print(" password: ", row[1])


slaves = cfg.slaves


def get_random_slave_ip_port():

    global slaves

    i = random.randint(0,len(slaves))

    ip = slaves[i][0]
    port = slaves[i][1]

    return ip, int(port)


def random_string(l):

    id = ""
    for x in range(l):
        id += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz')

    return id


def random_string_simple(l):

    id = ""
    for x in range(l):
        id += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    return id


# check if a session is valid
def check_session(s):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM session WHERE session_string = %s ", (s,))
    sessions = cur.fetchall()[0][0]
    return sessions


def get_user_id_from_session(s):
    # this should only be used by SLAVE, because user id is not unique in master
    try:
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id  FROM session WHERE session_string = %s ", (s,))
        id = cur.fetchall()[0][0]
    except:
        id = -1
    return id


def get_user_and_slave_id_from_session(s):
    # this should only be used by SLAVE, because user id is not unique in master
    try:
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, slave_id  FROM session WHERE session_string = %s ", (s,))
        arr = cur.fetchall()[0]
        id = arr[0]
        s = arr[1]
    except:
        id = -1
    return id, 2


# check if user and password correct
def check_login(u, p):

    conn = dba.get_connection()
    cur = conn.cursor()
    hash_object = hashlib.md5(p.encode())
    p_hash = hash_object.hexdigest()
    log.log_info("p=" + p)
    log.log_info("p_hash=" + p_hash)
    cur.execute("SELECT count(*)  FROM users WHERE email = %s AND password = %s", (u, p_hash))
    ret = cur.fetchall()[0][0]
    print(ret)
    return ret


# check if user exists
def check_user(u):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM users WHERE email = %s ", (u, ))
    ret = cur.fetchall()[0][0]
    return ret


def make_save_session(u):
    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id  FROM users WHERE email = %s ", (u,))
    user_id = cur.fetchall()[0][0]

    sql = "INSERT INTO session (user_id, session_string) VALUES (%s, %s);"
    s = random_string(20)
    cur.execute(sql, (user_id, s))
    conn.commit()
    return s


def get_user_id(u):
    # this should only be used by SLAVE
    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id  FROM users WHERE email = %s ", (u,))
    user_id = cur.fetchall()[0][0]

    return user_id


def get_slave_ip_port(user_id):
    # this can only be used by MASTER

    print("get_slave_ip_port(user_id)", user_id)

    user_id = user_id.strip().lower()

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT slave_id  FROM master_slave_mapping WHERE session_or_user = %s ", (user_id,))

    rs = cur.fetchall()

    ip = ""
    port = -1

    if len(rs) > 0:
        id = rs[0][0]
    else:
        id = ""

    print("get_slave_ip_port(user_id) id = ", id)

    if len(id) > 0:
        id = id.strip()
        arr = slaves[id]
        ip = arr[0]
        port = arr[1]

    return ip, port


def update_password(u, p):
    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "UPDATE users SET password = %s WHERE email = %s;"
    hash_object = hashlib.md5(p.encode())
    p_hash = hash_object.hexdigest()
    log.log_info("p=" + p)
    log.log_info("p_hash=" + p_hash)
    cur.execute(sql, (p_hash, u))
    conn.commit()


def register_user(u, p):
    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (email, password) VALUES (%s, %s);"
    hash_object = hashlib.md5(p.encode())
    p_hash = hash_object.hexdigest()
    log.log_info("p=" + p)
    log.log_info("p_hash=" + p_hash)
    cur.execute(sql, (u, p_hash))
    conn.commit()


def register_slave(session_or_user, slave):

    session_or_user = session_or_user.strip().lower()
    slave = slave.strip() # do not make this lower case !!!
    if len(session_or_user) > 3:
        conn = dba.get_connection()
        cur = conn.cursor()
        #sql = "DELETE FROM master_slave_mapping WHERE session_or_user = %s;"
        #cur.execute(sql, (session_or_user, ))
        #conn.commit()
        sql = "INSERT INTO master_slave_mapping (session_or_user, slave_id) VALUES (%s, %s);"
        cur.execute(sql, (session_or_user, slave))
        conn.commit()
    else:
        log.log_error("cannot register register_slave(session_or_user, slave) because session_or_user too short: " + str(session_or_user))


def get_slave_id_from_session_or_user(s):
    # this should only be used by MASTER,
    s = str(s).strip().lower()
    try:
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT slave_id  FROM master_slave_mapping WHERE session_or_user = %s ", (s,))
        arr = cur.fetchall()[0]
        id = str(arr[0])
    except:
        id = ""
    return id.strip()


def insert_into_db(ip, time_stamp, delta_last_all, delta_last_this, is_https):

    sql = """
        INSERT INTO 
            traffic 
            (ip_address, time_stamp, delta_this_ip_last, delta_all_last, https) 
        VALUES 
            (%s, %s, %s, %s, %s);        
        
        """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (ip, time_stamp, delta_last_this, delta_last_all, is_https))
    conn.commit()


def insert_ip_loction(ip, time_stamp, location):
    sql = """
        INSERT INTO 
            ip_to_location 
            (ip_address, time_stamp, json) 
        VALUES 
            (%s, %s, %s);        

        """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (ip, time_stamp, location))
    conn.commit()
