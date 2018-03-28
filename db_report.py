#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random


def get_simple_report(user_id):

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = false AND count_positive < 1 AND direction = TRUE", (user_id,))
    new_words = cur.fetchall()[0][0]

    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = false AND count_positive > 0 AND direction = TRUE",
                (user_id,))
    learned_words = cur.fetchall()[0][0]

    return new_words, learned_words