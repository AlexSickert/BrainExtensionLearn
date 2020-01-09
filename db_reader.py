#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random
from datetime import datetime
from datetime import timedelta
import time


def create_progress_table():
    sql = """

    CREATE TABLE IF NOT EXISTS reader_texts
    (
      id SERIAL,
      user_id bigint,
      language character(50),
      url varchar(1000),
      timestamp bigint,
      title varchar(150),
      content text, 
      read BOOLEAN
    )
    WITH (
      OIDS=FALSE
    );

    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def save_text(user_id, language, url, text):

    try:
        time_stamp = int(time.time())

        title = text[0:70]

        sql = """
    
        INSERT INTO reader_texts 
        (user_id, language, url, timestamp, content, read, title) 
        values(%s, %s, %s, %s, %s, %s, %s);
    
        """
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (user_id, language, url, time_stamp, text, False, title))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as ex:

        log.log_error("save_text(user_id, language, url, text)  - part 1 " + str(ex))
        return -1, "part 1 - " + str(ex)


    try:
        sql = """
            SELECT max(id) FROM reader_texts WHERE user_id = %s LIMIT 2; 
        """

        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (user_id,))

        arr = cur.fetchall()

        cur.close()
        conn.close()

        return arr[0][0], ""

    except Exception as ex:

        log.log_error("save_text(user_id, language, url, text) - part 2 " + str(ex))
        return -1, "part 2 - " + str(ex)



def get_text_titles(user_id):

    log.log_info("get_text_titles(user_id): for user " + str(user_id))

    conn = dba.get_connection()
    cur = conn.cursor()

    sql = """
    
    SELECT id, language, title FROM reader_texts WHERE user_id = %s ORDER BY read LIMIT 200; 
    
    """

    cur.execute(sql, (user_id,))

    arr = cur.fetchall()

    cur.close()
    conn.close()

    return arr


def get_one_text(id, user_id):

    log.log_info("get_one_text(user_id): for user " + str(user_id))

    conn = dba.get_connection()
    cur = conn.cursor()

    sql = """

    SELECT content, id FROM reader_texts WHERE user_id = %s and id = %s LIMIT 1; 

    """

    cur.execute(sql, (user_id,id))

    arr = cur.fetchall()

    cur.close()
    conn.close()

    return arr[0][0], arr[0][1]


def set_text_read(id, user_id):

    sql = """

       UPDATE reader_texts 
       SET read = true WHERE id = %s and user_id = %s
       
       """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (id, user_id))
    conn.commit()
    cur.close()
    conn.close()


def add_to_progress(user_id, parameter_id, parameter_value):

    global progress_table_created

    if not progress_table_created:
        create_progress_table()

    time_stamp = int(time.time())

    sql = """

    INSERT INTO progress_history (user_id, parameter_id, time_stamp_server, parameter_value) values(%s, %s, %s, %s);
    
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql,(user_id, parameter_id, time_stamp, parameter_value))
    conn.commit()
    conn.close()



# run at startup to ensure table exists
create_progress_table()






