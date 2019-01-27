#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import time

print("loading db_add_content.py")


def add_spreadsheet_list(user_id, language, language_translation, list_obj):

    """
    uses the json object that was received by google spreadsheet and adds the words to the database
    :param user:
    :param language:
    :param list_obj:
    :return:
    """


    # create the ID of this insert.
    time_stamp = int(time.time())


    log.log_info("add_spreadsheet_list adding words... ")

    for row in list_obj:
        context = row[0]
        voc = row[1]
        trans = row[2]
        text = row[3]

        if len(voc) > 0:
            if len(trans) > 0:

                add_one_word_txt(user_id, language, voc, language_translation, trans, True, context, text, time_stamp)

                add_one_word_txt(user_id, language_translation, trans, language, voc, False, context, text, time_stamp)

    return ""


def add_one_word_txt(user_id, language_word, word, language_translation, translation, direction, context, text, time_stamp):

    # ToDo: This decoding should not be done here as it makes the whole process slower.

    language_word = get_language_code(language_word)
    language_translation = get_language_code(language_translation)

    add_one_word(user_id, language_word, word, language_translation, translation, direction, context, text, time_stamp)


def add_one_word(user_id, language_word, word, language_translation, translation, direction, context, text, time_stamp):

    """
    Add one single word and its translation
    :param user_id:
    :param language:
    :param word:
    :param translation:
    :return:
    """

    word = word.strip()

    if word_exists(user_id, language_word, word, language_translation):
        # print("word existst")
        update_word(user_id, language_word, word, language_translation, translation, context, text)
        return
    else:
        # print("new word")
        conn = get_connection()
        cur = conn.cursor()
        sql = "insert into vocabulary (example_sentences, context, user_id, language_word, word, language_translation," \
              " translation, direction, count_positive, count_negative, current, upload_batch) " \
              "values (%s, %s, %s, %s , %s, %s, %s, %s, 0, 0, 'FALSE', %s);"
        if direction == True:
            cur.execute(sql, (text, context, user_id, language_word, word, language_translation, translation, "TRUE", time_stamp))
        else:
            cur.execute(sql, (text, context, user_id, language_word, word, language_translation, translation, "FALSE", time_stamp))
        conn.commit()
        # print("done")

        # now check if done properly
        # Todo: remove this in future as it is only for testing and smapping the long file

        sql = "select id from vocabulary where user_id = %s and language_word = %s and word = %s and language_translation = %s and translation = %s"

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (user_id, language_word, word, language_translation, translation))


        arr = cur.fetchall()

        log.log_info("--- check if new word was inserted ---")

        for r in arr:
            log.log_info("newly inserted word as id: " + str(r[0]))

        log.log_info("--------------------------------------")

    return


def get_connection():
    """
    gets the database connection.
    :return:
    """

    hostname = cfg.parameters["hostname"]
    username = cfg.parameters["username"]
    password = cfg.parameters["password"]
    database = cfg.parameters["database"]

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    conn.set_client_encoding('UTF8')

    return conn


def update_word(user_id, language_word, word, language_translation, translation, context, text):

    """
    Gets executed when user is uploading from google spreadsheet
    :param user_id:
    :param language_word:
    :param word:
    :param language_translation:
    :param translation:
    :param context:
    :param text:
    :return:
    """

    word = word.strip()

    conn = get_connection()
    cur = conn.cursor()
    sql = "update vocabulary set translation = %s where user_id = %s and language_word = %s and word = %s and language_translation = %s  and edited = false;"
    cur.execute(sql, (translation, user_id, language_word, word, language_translation))
    conn.commit()

    sql = "update vocabulary set context = %s where user_id = %s and language_word = %s and word = %s and language_translation = %s  and edited = false;"
    cur.execute(sql, (context, user_id, language_word, word, language_translation))
    conn.commit()

    sql = "update vocabulary set example_sentences = %s where user_id = %s and language_word = %s and word = %s and language_translation = %s and edited = false;"
    cur.execute(sql, (text, user_id, language_word, word, language_translation))
    conn.commit()

    return True


def update_word_by_id(user_id, word, translation, word_id):

    """
    This gets executed if user is manually editing the word on the mobile device
    :param user_id:
    :param word:
    :param translation:
    :param word_id:
    :return:
    """

    # ToDo: here is a proper error handling msissing if update fails.

    word = word.strip()

    conn = get_connection()
    cur = conn.cursor()
    sql = "update vocabulary set translation = %s, word = %s, edited = true where user_id = %s and id = %s ;"
    cur.execute(sql, (translation, word, user_id, word_id))
    conn.commit()


    return True

def word_exists(user_id, language_word, word, language_translation):

    """
    checks if a word exists
    :param user:
    :param language:
    :param word:
    :return: true or false
    """

    word = word.strip()

    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT count(*)  FROM vocabulary where user_id = %s and word = %s and language_word = %s and language_translation = %s"
    cur.execute(sql, (user_id, word, language_word, language_translation))

    l = cur.fetchall()[0][0]

    if l > 0:
        return True
    else:
        return False


def get_language_label(n):

    if n == 1:
        return "English"
    if n == 2:
        return "Spanish"
    if n == 3:
        return "German"
    if n == 4:
        return "Russian"
    if n == 5:
        return "Italian"
    if n == 6:
        return "Portuguese"
    if n == 7:
        return "French"

def get_language_code(str):

    """
    convert the language strings into language codes to make database more compact
    ToDo: make this a database table that gets loaded on startup
    :param str:
    :return:
    """

    s = str.strip().lower()

    if s == "english":
        return 1
    if s == "en":
        return 1
    if s == "engl":
        return 1

    if s == "spanish":
        return 2
    if s == "es":
        return 2
    if s == "span":
        return 2

    if s == "german":
        return 3
    if s == "de":
        return 3
    if s == "deutsch":
        return 3

    if s == "russian":
        return 4
    if s == "ru":
        return 4
    if s == "rus":
        return 4

    if s == "italian":
        return 5
    if s == "it":
        return 5
    if s == "ital":
        return 5
    if s == "italiano":
        return 5

    if s == "portuguese":
        return 6
    if s == "pt":
        return 6
    if s == "port":
        return 6
    if s == "portugese":
        return 6

    if s == "french":
        return 7
    if s == "fr":
        return 7
    if s == "franz":
        return 7

    return 99



