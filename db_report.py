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


def get_report_charts(user_id):

    l, v = get_report_chart(user_id)
    c1 = dict()
    c1["labels"] = l
    c1["values"] = v

    l, v = get_report_chart(user_id)
    c2 = dict()
    c2["labels"] = l
    c2["values"] = v

    l, v = get_report_chart(user_id)
    c3 = dict()
    c3["labels"] = l
    c3["values"] = v

    l, v = get_report_chart(user_id)
    c4 = dict()
    c4["labels"] = l
    c4["values"] = v

    return c1, c2, c3, c4


def get_report_chart(user_id):

    today = datetime.now().date()
    values = []
    labels = []
    r = 8
    for i in range(r):

        delta = (r - i - 1) * -1

        date_check = today + timedelta(days=delta)

        v = random.randint(0, 200)

        if delta == 0:
            values.append(v)
            labels.append("today")
        else:
            values.append(v)
            labels.append(datetime.strftime(date_check, "%d.%m."))
    return labels, values


def get_simple_report(user_id):

    log.log_info("get_simple_report(user_id): for user " + str(user_id))

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = false AND count_positive < 1 AND direction = TRUE", (user_id,))
    new_words = cur.fetchall()[0][0]

    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = false AND count_positive > 0 AND direction = TRUE",
                (user_id,))
    learned_words = cur.fetchall()[0][0]

    parameter_name = "percentage_learned"

    sql = "SELECT value FROM parameters WHERE user_id = %s AND key = %s"
    cur.execute(sql, (user_id, parameter_name))

    try:
        arr = cur.fetchall()
        p = arr[0][0]
        log.log_info("value from rs is: " + str(p))
    except:
        log.log_info("value rs is not existing: " )
        p = 0.0

    ratio_learned = float(p) * 100
    ratio_learned = round(ratio_learned, 2)

    log.log_info("ratio_learned at end is is: " + str(ratio_learned))

    return new_words, learned_words, ratio_learned


progress_table_created = False


def create_progress_table():
    """
    parameter_id:
        1 is for percentage learnd
        2 is for ...
        3 is for ...

    """
    sql = """
    
    CREATE TABLE IF NOT EXISTS progress_history
    (
      user_id bigint,
      parameter_id bigint,
      time_stamp_server bigint,
      parameter_value numeric
    )
    WITH (
      OIDS=FALSE
    );
    
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
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









