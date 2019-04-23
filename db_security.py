#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random
import hashlib
import time


slaves = cfg.slaves
slaves_arr = cfg.slaves_arr


def get_random_slave_ip_port():

    global slaves_arr

    log.log_info("length of slaves_arr: " + str(len(slaves_arr)))
    i = random.randint(0,len(slaves)-1)

    ip = slaves_arr[i][1]
    port = slaves_arr[i][2]

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

    if u in ["user-1@data-yield.com", "user-2@data-yield.com", "monitoring@data-yield.com"]:
        s = random_string(10) + "$testuser$"
    else:
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


def get_users():
    """
    get all users - not byu id, but by their email address
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()

    ret = []

    cur.execute("SELECT distinct email  FROM users ")
    arr = cur.fetchall()

    for row in arr:
        #print(row[0])
        ret.append(str(row[0]).strip())

    return ret


def debug_master_slave_mapping():

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT slave_id, session_or_user  FROM master_slave_mapping ")
    rs = cur.fetchall()
    log.log_info("---------------------------------")
    log.log_info("master slave mapping: ")

    for r in rs:
        log.log_info("row: " + str(r))

    log.log_info("---------------------------------")


def get_slave_ip_port(user_id):
    # this can only be used by MASTER

    log.log_info("get_slave_ip_port(user_id)" + str(user_id))

    user_id = str(user_id).strip().lower()

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
        log.log_info("get_slave_ip_port(user_id) - got empty rs for id = " + str(id))
        debug_master_slave_mapping()

    if len(id) > 0:
        id = id.strip()
        arr = slaves[id]
        ip = arr[0]
        port = arr[1]
    else:
        # we have a problem and debug the values
        debug_master_slave_mapping()

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


def register_slave(session_or_user, slave, user_email):

    session_or_user = session_or_user.strip().lower()
    slave = slave.strip() # do not make this lower case !!!
    ts = time.time()

    if len(session_or_user) > 3:

        conn = dba.get_connection()
        cur = conn.cursor()
        sql = "DELETE FROM master_slave_mapping WHERE session_or_user = %s;"
        cur.execute(sql, (session_or_user, ))
        conn.commit()

        #sql = "INSERT INTO master_slave_mapping (session_or_user, slave_id, user_email, time_stamp) VALUES (%s, %s, %s, %s);"
        #cur.execute(sql, (session_or_user, slave, user_email, ts))

        sql = "INSERT INTO master_slave_mapping (session_or_user, slave_id) VALUES (%s, %s);"
        cur.execute(sql, (session_or_user, slave))

        conn.commit()

    elif len(user_email) > 3:

        conn = dba.get_connection()
        cur = conn.cursor()
        sql = "DELETE FROM master_slave_mapping WHERE session_or_user = %s;"
        cur.execute(sql, (session_or_user,))
        conn.commit()

        # sql = "INSERT INTO master_slave_mapping (session_or_user, slave_id, user_email, time_stamp) VALUES (%s, %s, %s, %s);"
        # cur.execute(sql, (session_or_user, slave, user_email, ts))

        sql = "INSERT INTO master_slave_mapping (session_or_user, slave_id) VALUES (%s, %s);"
        cur.execute(sql, (user_email, slave))

        conn.commit()

    else:
        log.log_error("cannot register register_slave(session_or_user, slave) because session_or_user or user_email too short: " + str(session_or_user))
        log.log_error("session_or_user : " + str(session_or_user))
        log.log_error("user_email : " + str(user_email))



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


def get_ip_to_location():

    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "SELECT distinct ip_address, json from ip_to_location limit 1000"
    cur.execute(sql)
    arr = cur.fetchall()
    return arr


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
