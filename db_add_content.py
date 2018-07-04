#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log

print("loading db_add_content.py")


def add_spreadsheet_list(user_id, language, language_translation, list_obj):

    """
    uses the json object that was received by google spreadsheet and adds the words to the database
    :param user:
    :param language:
    :param list_obj:
    :return:
    """

    lang_code = get_language_code(language)

    log.log_info("add_spreadsheet_list adding words... ")

    for row in list_obj:
        context = row[0]
        voc = row[1]
        trans = row[2]

        if len(voc) > 0:
            if len(trans) > 0:

                add_one_word_txt(user_id, language, voc, language_translation, trans, True, context)

                add_one_word_txt(user_id, language_translation, trans, language, voc, False, context)

    return ""


def add_one_word_txt(user_id, language_word, word, language_translation, translation, direction, context):

    language_word = get_language_code(language_word)
    language_translation = get_language_code(language_translation)

    add_one_word(user_id, language_word, word, language_translation, translation, direction, context)


def add_one_word(user_id, language_word, word, language_translation, translation, direction, context):

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
        update_word(user_id, language_word, word, language_translation, translation, context)
        return
    else:
        # print("new word")
        conn = get_connection()
        cur = conn.cursor()
        sql = "insert into vocabulary (context, user_id, language_word, word, language_translation," \
              " translation, direction, count_positive, count_negative, current) " \
              "values (%s, %s, %s, %s , %s, %s, %s, 0, 0, 'FALSE');"
        if direction == True:
            cur.execute(sql, (context, user_id, language_word, word, language_translation, translation, "TRUE"))
        else:
            cur.execute(sql, (context, user_id, language_word, word, language_translation, translation, "FALSE"))
        conn.commit()
        # print("done")
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

    return conn


def update_word(user_id, language_word, word, language_translation, translation, context):

    word = word.strip()

    conn = get_connection()
    cur = conn.cursor()
    sql = "update vocabulary set translation = %s where user_id = %s and language_word = %s and word = %s and language_translation = %s;"
    cur.execute(sql, (translation, user_id, language_word, word, language_translation))
    conn.commit()

    sql = "update vocabulary set context = %s where user_id = %s and language_word = %s and word = %s and language_translation = %s;"
    cur.execute(sql, (context, user_id, language_word, word, language_translation))
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



