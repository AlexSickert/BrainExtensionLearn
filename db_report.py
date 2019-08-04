#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random


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

