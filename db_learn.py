#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random


def process_answer(word_id, user_id, answer):

    """
    ToDo: the user ID is not used here and this allows the user to access other people's data. it is a security hole

    :param word_id:
    :param user_id:
    :param answer:
    :return:
    """

    log.log_info("process_answer " + answer)

    if answer == "YES":

        n = get_yes(word_id)
        n = int(n) + 1

        sql = "UPDATE vocabulary SET count_positive = %s WHERE id = %s "
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (n, word_id) )
        conn.commit()

        # now check if we need to move the word to the 'learned' category
        if check_if_learned(word_id):
            sql = "UPDATE vocabulary SET current = FALSE WHERE id = %s "
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(sql, (word_id,))
            conn.commit()

    if answer == "NO":

        n = get_no(word_id)
        n = int(n) + 1

        sql = "UPDATE vocabulary SET count_negative = %s WHERE id = %s "
        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (n, word_id) )
        conn.commit()


def check_if_learned(word_id):

    """
    checks if we know the word well enough
    :param word_id:
    :return:
    """

    y = get_yes(word_id)
    n = get_no(word_id)

    if y > n +2:
        return True
    else:
        return False


def get_next_word_id(user_id, last_word_id):



    if count_current(user_id) < 7:
        log.log_info("get_next_word_id - count_current less than 7" )
        # we need to add a new word question is if repeat old word or use new
        while count_current(user_id) < 7:
            if add_new_word():
                # ToDo: if there are no new words left, then we need to process old words and send info to user,
                # that there are no new words left

                if count_not_learned(user_id) > 0:
                    word_id = get_new_random(user_id)
                else:
                    # if there are no new words left then use old words
                    word_id = get_old_random(user_id)

            else:
                # we can add old only if such words exist
                # if not, then we add from new category
                num_learned = count_learned(user_id)
                if num_learned > 0:
                    word_id = get_old_random(user_id)
                else:
                    word_id = get_new_random(user_id)


            set_word_current(word_id)

        """
        ToDo: This here is not good because we might return null value
        """
        return word_id
    else:
        # we only need to pick a random word from the 7 words
        log.log_info("get_next_word_id - pick one word from 7")

        if len(last_word_id) > 0:

            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT ID  FROM vocabulary where user_id = %s AND current = true AND id <> %s ORDER BY random() LIMIT 1",
                (user_id,last_word_id))
            l = cur.fetchall()[0][0]
        else:
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT ID  FROM vocabulary where user_id = %s AND current = true ORDER BY random() LIMIT 1",
                (user_id, ))
            l = cur.fetchall()[0][0]
        return l


def get_word(new_id):

    """
    id, l1, w1, l2, w2 = dbl.get_word(new_id)
    :param new_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()

    sql = ""
    sql += "SELECT ID, language_word, word, language_translation, translation FROM vocabulary "
    sql += "WHERE ID = %s "

    cur.execute(sql,(new_id, ))

    arr = cur.fetchall()

    id = arr[0][0]
    l1 = arr[0][1]
    w1 = str(arr[0][2]).strip()
    l2 = arr[0][3]
    w2 = str(arr[0][4]).strip()

    return id, l1, w1, l2, w2



def set_word_current(word_id):
    """

    :param word_id:
    :return:
    """

    log.log_info("set_word_current " + str(word_id))

    sql = "UPDATE vocabulary SET current = TRUE WHERE id = %s "
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (word_id, ))
    conn.commit()


def get_old_random(user_id):
    """
    get a new word from the pile of words so far not studied by random

    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    # cur.execute(
    #     "SELECT ID  FROM vocabulary where user_id = %s AND current = FALSE AND count_positive > 0 ORDER BY random() LIMIT 1",
    #     (user_id,))

    sql = """
    
    select id, (count_negative::float + 1) / count_positive::float as ratio  
    FROM
    vocabulary
    where
    user_id = %s AND 
    current = false
    AND
    count_positive > 0
    order
    by
    ratio
    desc
    limit
    3;   
    
    """

    cur.execute(sql, (user_id,))

    l = cur.fetchall()[0][0]
    return l


def get_new_random(user_id):
    """
    get a new word from the pile of words so far not studied by random

    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vocabulary where user_id = %s AND current = FALSE AND direction = TRUE AND count_positive = 0 ORDER BY random() LIMIT 1", (user_id,))
    l = cur.fetchall()[0][0]
    return l


def add_new_word():
    """
    Decide if we want to add a word from the pile of new words or from the pile of old words that need repetition
    :return:
    """

    r = random.random()

    if r > 0.5:
        return True
    else:
        return False


def count_current(user_id):
    """

    :param user_id:
    :return:
    """
    log.log_info("count_current")
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = true", (user_id,) )
    l = cur.fetchall()[0][0]
    return int(l)


def get_yes(word_id):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count_positive  FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]
    return l


def get_no(word_id):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count_negative  FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]
    return l

def count_learned(user_id):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where count_positive > 0 AND user_id = %s", (user_id,) )
    l = cur.fetchall()[0][0]
    return l

def count_not_learned(user_id):
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where current = false AND count_positive < 1 AND direction = TRUE AND user_id = %s", (user_id,) )
    l = cur.fetchall()[0][0]
    return l
