#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random
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
    try:
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id  FROM session WHERE session_string = %s ", (s,))
        id = cur.fetchall()[0][0]
    except:
        id = -1
    return id

# check if user and password correct
def check_login(u, p):

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM users WHERE email = %s AND password = %s", (u, p))
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
    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id  FROM users WHERE email = %s ", (u,))
    user_id = cur.fetchall()[0][0]

    return user_id

def update_password(u, p):
    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "UPDATE users SET password = %s WHERE email = %s;"
    cur.execute(sql, (p, u))
    conn.commit()


def register_user(u, p):
    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (email, password) VALUES (%s, %s);"
    cur.execute(sql, (u, p))
    conn.commit()

