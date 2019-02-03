#!/usr/bin/env python

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import db_add_content as dba
import random
import time

short_term_memory_length = 10


def process_answer_ordered(word_id, user_id, answer):

    """
    ToDo: the user ID is not used here and this allows the user to access other people's data. it is a security hole

    This method was developed January 2019

    This function is used by

    :param word_id:
    :param user_id:
    :param answer:
    :return: if the answer lead to a success in terms of leanring
    """

    global short_term_memory_length

    success = False
    experiment = False
    once_learned = False

    # ToDo: the user ID is not used here and this allows the user to access other people's data. it is a security hole

    log.log_info("process_answer " + answer)

    #before we update the data in the database, we need to process the result incase it was an experiment

    if len(str(word_id)) > 0:
        experiment, once_learned = process_experiment(word_id, user_id, answer)

        experiment_timestamp = int(time.time())

        # set timestamp of last access
        sql = "UPDATE vocabulary SET last_studied = %s WHERE id = %s "

        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (experiment_timestamp, word_id))
        conn.commit()

        position = get_position(word_id)

        log.log_info("position up to now " + str(position))

        if answer == "YES":

            if experiment:
                # it was an experiment and it was a success so we can push it to the "done" category
                position = short_term_memory_length + 2
            else:
                position = position + 1

            n = get_yes(word_id)
            n = int(n) + 1
            pn = "y" + get_np_string(word_id)
            pn = pn[0:240]

            sql = "UPDATE vocabulary SET count_positive = %s , pn_string = %s WHERE id = %s "
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(sql, (n, pn, word_id) )
            conn.commit()

            # now check if we need to move the word to the 'learned' category
            #if check_if_learned(word_id):
            if check_if_learned_ordered(word_id, experiment):
                sql = "UPDATE vocabulary SET current = FALSE WHERE id = %s "
                conn = dba.get_connection()
                cur = conn.cursor()
                cur.execute(sql, (word_id,))
                conn.commit()
                success = True

        if answer == "NO":

            if experiment:
                position = int(short_term_memory_length / 2)
            else:
                if position > 3:
                    position = int(position / 2)
                else:
                    position = 1

            n = get_no(word_id)
            n = int(n) + 1
            pn = "n" + get_np_string(word_id)
            pn = pn[0:240]
            sql = "UPDATE vocabulary SET count_negative = %s , pn_string = %s WHERE id = %s "
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(sql, (n, pn, word_id) )
            conn.commit()

        # update the position
        log.log_info("new position " + str(position))
        set_position(word_id, position)


        if experiment:
            if not success:
                # forgot the word
                add_transition(word_id, user_id, 2)

        else:
            if once_learned:
                # re-learned existing word
                add_transition(word_id, user_id, 3)

            else:
                # learned new word
                add_transition(word_id, user_id, 1)

        add_to_history(user_id, word_id, answer)

    # success flag is needed to decide if we make a toast on the client app or not
    return success, experiment, once_learned


def process_answer(word_id, user_id, answer):

    """
    ToDo: the user ID is not used here and this allows the user to access other people's data. it is a security hole

    This method was used ontil end of 2018. Now new method

    This function is used by

    :param word_id:
    :param user_id:
    :param answer:
    :return: if the answer lead to a success in terms of leanring
    """

    success = False
    experiment = False
    once_learned = False

    # ToDo: the user ID is not used here and this allows the user to access other people's data. it is a security hole

    log.log_info("process_answer " + answer)

    #before we update the data in the database, we need to process the result incase it was an experiment

    if len(str(word_id)) > 0:
        experiment, once_learned = process_experiment(word_id, user_id, answer)

        experiment_timestamp = int(time.time())

        # set timestamp of last access
        sql = "UPDATE vocabulary SET last_studied = %s WHERE id = %s "

        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (experiment_timestamp, word_id))
        conn.commit()

        if answer == "YES":

            n = get_yes(word_id)
            n = int(n) + 1
            pn = "y" + get_np_string(word_id)
            pn = pn[0:240]

            sql = "UPDATE vocabulary SET count_positive = %s , pn_string = %s WHERE id = %s "
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(sql, (n, pn, word_id) )
            conn.commit()

            # now check if we need to move the word to the 'learned' category
            if check_if_learned(word_id):
                sql = "UPDATE vocabulary SET current = FALSE WHERE id = %s "
                conn = dba.get_connection()
                cur = conn.cursor()
                cur.execute(sql, (word_id,))
                conn.commit()
                success = True

        if answer == "NO":

            n = get_no(word_id)
            n = int(n) + 1
            pn = "n" + get_np_string(word_id)
            pn = pn[0:240]
            sql = "UPDATE vocabulary SET count_negative = %s , pn_string = %s WHERE id = %s "
            conn = dba.get_connection()
            cur = conn.cursor()
            cur.execute(sql, (n, pn, word_id) )
            conn.commit()

        if experiment:
            if not success:
                # forgot the word
                add_transition(word_id, user_id, 2)

        else:
            if once_learned:
                # re-learned existing word
                add_transition(word_id, user_id, 3)

            else:
                # learned new word
                add_transition(word_id, user_id, 1)

        add_to_history(user_id, word_id, answer)

    # success flag is needed to decide if we make a toast on the client app or not
    return success, experiment, once_learned


def get_calc_rank(word_id):

    sql = "SELECT calc_rank from vocabulary WHERE id = %s"

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (word_id,))

    try:
        arr = cur.fetchall()
        e = arr[0][0]
    except:
        e = 0
    return e


def add_to_history(user_id, word_id, answer):

    r = get_calc_rank(word_id)

    if answer == "YES":
        result = True
    else:
        result = False

    sql = """ 

           INSERT INTO history 
           (
               user_id,
               word_id,
               result,
               time_stamp_server,
               calc_rank                 
           )
           VALUES
           (
               %s, %s, %s, %s, %s
           )   

           """

    time_stamp = int(time.time())

    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute(sql, (user_id,
                      word_id,
                      result,
                      time_stamp,
                      r))
    conn.commit()


def add_transition(word_id, user_id, transition):

    sql = """ 

       INSERT INTO transitions 
       (
           user_id,
           word_id,
           time_stamp,
           transition  
       )
       VALUES
       (
           %s, %s, %s, %s
       )   

       """

    time_stamp = int(time.time())

    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute(sql, (user_id,
                      word_id,
                      time_stamp,
                      transition
                      ))
    conn.commit()


def experiment_counter(word_id):

    sql = """ 

        SELECT 
            count_experiments,
            count_forgotten 
        FROM
            vocabulary
        WHERE
            id = %s   

        """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (word_id,))

    try:
        arr = cur.fetchall()
        e = arr[0][0]
        f = arr[0][1]
    except:
        e = 0
        f = 0

    return e, f


def process_experiment(word_id, user_id, answer):

    """
    In essences, the function copies a line from the vocabulary table and inserts it in the experiments table
    In addition, it enriches the data with a timestamp and if the experiment was sucessfull.
    successful = user knows the word, unsuccessful = user forgot the word
    :param word_id:
    :param user_id:
    :param answer:
    :return:
    """

    exp, forg = experiment_counter(word_id)

    sql = """ 
    
    SELECT 
        is_experiment,
        pn_string,
        count_positive,
        count_negative,
        last_studied,    
        average_pos_length,
        max_pos_length ,
        last_pos_length ,
        pos_neg_length_ratio ,
        count_positive ,
        count_negative ,
        user_id ,
        direction ,
        language_word,
        language_translation,        
        current,
        once_successfully_learned,
        calc_rank 
    FROM
        vocabulary
    WHERE
        id = %s   
    
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (word_id, ))

    arr = cur.fetchall()

    is_experiment = arr[0][0]

    once_learned = arr[0][16]


    if is_experiment:

        pn_string = arr[0][1]
        count_positive = arr[0][2]
        count_negative = arr[0][3]
        last_studied = arr[0][4]
        average_pos_length = arr[0][5]
        max_pos_length = arr[0][6]
        last_pos_length = arr[0][7]
        pos_neg_length_ratio = arr[0][8]
        count_positive = arr[0][9]
        count_negative = arr[0][10]
        user_id = arr[0][11]
        direction = arr[0][12]
        language_word = arr[0][13]
        language_translation = arr[0][14]
        calc_rank = arr[0][17]


        sql = """ 
        
            INSERT INTO experiments 
            (
                pn_string,
                count_positive,
                count_negative,
                last_studied,
                average_pos_length,
                max_pos_length,
                last_pos_length,
                pos_neg_length_ratio,
                user_id,
                direction,
                language_word,
                language_translation,              
                experiment_timestamp,
                word_id,
                success,
                calc_rank
            
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s
            )   
        
            """

        experiment_timestamp = int(time.time())

        if answer == "YES":
            answer = True
        else:
            answer = False

        update_vocabulary_counter(word_id, exp, forg, answer)

        cur.execute(sql, (pn_string,
                count_positive,
                count_negative,
                last_studied,
                average_pos_length,
                max_pos_length,
                last_pos_length,
                pos_neg_length_ratio,
                user_id,
                direction,
                language_word,
                language_translation,
                experiment_timestamp,
                word_id, answer, calc_rank ))
        conn.commit()

    # remove the experiment flag
    set_experiment_state(word_id, False)


    return is_experiment, once_learned


def update_vocabulary_counter(word_id,  experiment, forgotten, answer):

    if answer == False:
        forgotten += 1

    experiment += 1

    sql = """
        UPDATE 
            vocabulary
        SET 
            count_experiments = %s,
            count_forgotten = %s
        WHERE 
            id = %s 
          """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (experiment, forgotten, word_id))
    conn.commit()

def set_experiment_state(word_id, is_experiment):

    """
    we flag a word if it is in experiment state or not. Important is to remove the flag once the experiment is over.
    :param word_id:
    :param is_experiment:
    :return:
    """

    sql = "UPDATE vocabulary SET is_experiment = %s WHERE id = %s "
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (is_experiment, word_id))
    conn.commit()


def check_if_learned(word_id):

    """
    checks if we know the word well enough. This is the case if the positive answers are higher than the negative and
    if the last two answers were positive
    :param word_id:
    :return:
    """

    y = get_yes(word_id)
    n = get_no(word_id)

    if y > n +2:
        pn = get_np_string(word_id)
        if pn[0:2] == "yy":
            return True
        else:
            return False
    else:
        return False


def check_if_learned_ordered(word_id, is_experiment):

    """
    checks if we know the word well enough. This is the case if the positive answers are higher than the negative and
    if the postiion in the ordered short term memory is larger than 9, which actually means we need to know the word
    9 times in a row with no mistake

    :param word_id:
    :return:
    """

    y = get_yes(word_id)
    n = get_no(word_id)
    p = get_position(word_id)

    log.log_info("check_if_learned_ordered - y: " + str(y))
    log.log_info("check_if_learned_ordered - n: " + str(n))
    log.log_info("check_if_learned_ordered - p: " + str(p))

    # when we run an experiment then the p value can be different. therefore we set it high enough
    if is_experiment:
        p = 99

    if y > n +2:
        if p > 9:
            log.log_info("check_if_learned_ordered - return true")
            return True
        else:
            log.log_info("check_if_learned_ordered - return False")
            return False
    else:
        log.log_info("check_if_learned_ordered - return False II")
        return False


def get_next_word_id(user_id, last_word_id):
    """

    NOTE: consider also the function get_next_word_id_array(user_id, last_word_id) because it is similar !!!

    Loads the id of the next word we want to learn. This can be either one of the 7 in the caroussel or if the
    carousel is less than 7 we add another word and then learn this.

    :param user_id:
    :param last_word_id:
    :return:
    """

    count = count_current(user_id)

    if count < 7:
        log.log_info("get_next_word_id - count_current less than 7" )
        # we need to add a new word question is if repeat old word or use new

        do_continue = True
        tmp_count = 0

        while do_continue:

            if count_current(user_id) >= 7:
                do_continue = False

            tmp_count += 1

            # just to prevent endless loop
            if tmp_count > 14:
                log.log_error("get_next_word_id needed to abord because endless loop")
                do_continue = False

            if add_new_word():
                # ToDo: if there are no new words left, then we need to process old words and send info to user,
                # that there are no new words left

                if count_not_learned(user_id) > 0:
                    log.log_info("more than zero learned words")
                    word_id = get_new_random(user_id)
                else:
                    log.log_info("zero learned words")
                    # if there are no new words left then use old words
                    word_id = get_old_by_score(user_id)

            else:
                # we can add old only if such words exist
                # if not, then we add from new category
                num_learned = count_learned(user_id)
                if num_learned > 0:
                    log.log_info("num_learned more than zero")
                    word_id = get_old_by_score(user_id)
                else:
                    log.log_info("num_learned zero")
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


def get_next_word_id_array(user_id, last_word_id):
    """
    NOTE: consider also the funciton get_next_word_id(user_id, last_word_id) because it is similar !!!


    :param user_id:
    :param last_word_id:
    :return:
    """

    # first we ensure there are enough current words

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
                    word_id = get_old_by_score(user_id)

            else:
                # we can add old only if such words exist
                # if not, then we add from new category
                num_learned = count_learned(user_id)
                if num_learned > 0:
                    word_id = get_old_by_score(user_id)
                else:
                    word_id = get_new_random(user_id)


            set_word_current(word_id)


    # now we load all the current words as an array
    ret = []
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT ID  FROM vocabulary where user_id = %s AND current = true ORDER BY random() LIMIT 20",
        (user_id,))
    l = cur.fetchall()

    for id in l:
        ret.append(id[0])

    return ret


def get_next_word_id_array_ordered_position(user_id, last_word_id):
    """

    Januar 2019 new locic where we use a longer short term memeory and when user knows a word we increase the position
    of the word in an ordere table

    :param user_id:
    :param last_word_id:
    :return:
    """
    global short_term_memory_length
    # first we ensure there are enough current words

    if count_current(user_id) < short_term_memory_length:
        log.log_info("get_next_word_id - count_current less than 7" )
        # we need to add a new word question is if repeat old word or use new
        while count_current(user_id) < short_term_memory_length:
            if add_new_word():
                # ToDo: if there are no new words left, then we need to process old words and send info to user,
                # that there are no new words left

                if count_not_learned(user_id) > 0:
                    word_id = get_new_random(user_id)
                else:
                    # if there are no new words left then use old words
                    word_id = get_old_by_score(user_id)  # this is what we call an experiment

            else:
                # we can add old only if such words exist
                # if not, then we add from new category
                num_learned = count_learned(user_id)
                if num_learned > 0:
                    word_id = get_old_by_score(user_id) # this is what we call an experiment
                else:
                    word_id = get_new_random(user_id)


            set_word_current(word_id)


    # now we load all the current words as an array
    ret = []
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("""
    
    SELECT 
        ID, COALESCE(short_memory_position, 1)  
    FROM 
        vocabulary 
    where 
        user_id = %s AND current = true 
        and direction = TRUE
    ORDER BY 
        COALESCE(short_memory_position, 1) ,
        last_studied     
        
    LIMIT """ + str(short_term_memory_length + 1), (user_id,))
    l = cur.fetchall()

    for id in l:
        if id[1] is None:
            pos = 1
        else:
            pos = id[1]

        ret.append([id[0], pos])

        log.log_info(str(id[0]) + " => " + str(pos))

    return ret


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

    sql = "UPDATE vocabulary SET current = TRUE, short_memory_position = 1 WHERE id = %s "
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (word_id, ))
    conn.commit()


def get_old_by_score(user_id):
    """
    take one word from the pile of words we already learned

    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()


    sql = """

        SELECT 
            id, calc_rank 
        FROM
            vocabulary
        WHERE
            user_id = %s 
        AND 
            current = false
        AND
            count_positive > 0
        ORDER BY    
            calc_rank desc
        LIMIT 2;   

        """

    cur.execute(sql, (user_id,))

    #l = cur.fetchall()[0][0]

    arr = cur.fetchall()
    print(arr)

    if len(arr) > 0:

        i = int(random.random() * float(len(arr)))
        l = arr[i][0]
        set_experiment_state(l, True)
    else:
        l = -1

    log.log_info("get_old_by_score returns " + str(l) + " for user id " + str(user_id))

    return l


def get_new_random(user_id):
    """
    get a new word from the pile of words so far not studied by random

    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM vocabulary where user_id = %s AND current = FALSE AND direction = TRUE AND count_positive < 1 ORDER BY random() LIMIT 1", (user_id,))

    arr = cur.fetchall()

    if len(arr) > 0:
        l = arr[0][0]
    else:
        l = -1

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
    Counts how many words are in the carousel for a specific user.
    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where user_id = %s AND current = true", (user_id,) )
    l = cur.fetchall()[0][0]
    log.log_info("count_current is " + str(l))
    return int(l)


def get_yes(word_id):
    """
    Get for a specific word the number of positive answers
    :param word_id:
    :return:
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count_positive  FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]
    return l


def get_position(word_id):
    """
    Get the short term memory position of the word
    :param word_id:
    :return:
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(short_memory_position, 1)    FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]

    if l is None:
        l = 1

    return int(l)

def set_position(word_id, pos):

    log.log_info("set_position " + str(word_id) + " to " + str(pos))

    sql = "UPDATE vocabulary SET short_memory_position = %s WHERE id = %s "
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (pos, word_id))
    conn.commit()


def get_np_string(word_id):
    """
    Get for a specific word the the string that looks like ynnyynynyynnynyn
    :param word_id:
    :return:
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT pn_string  FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]

    if not l:
        l = ""

    return l


def get_no(word_id):
    """
    Get for a specific word the number of negative answers
    :param word_id:
    :return:
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count_negative  FROM vocabulary where ID = %s", (word_id,) )
    l = cur.fetchall()[0][0]
    return l


def count_learned(user_id):
    """
    count the number of words that were already successfully learned
    :param user_id:
    :return:
    """
    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where count_positive > 0 AND user_id = %s", (user_id,) )
    l = cur.fetchall()[0][0]
    return l


def count_not_learned(user_id):
    """
    Counts the number of words so far not learned
    :param user_id:
    :return:
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*)  FROM vocabulary where current = false AND count_positive < 1 AND direction = TRUE AND user_id = %s", (user_id,) )
    l = cur.fetchall()[0][0]
    return l
