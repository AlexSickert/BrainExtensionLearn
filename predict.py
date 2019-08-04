"""

This script runs the prediction. It is the central point of the application in the sense that everything else is
more or less just infrastructure. Here is the magic point where we predict which worked will be forgotten soon.


"""

import psycopg2
import sys, traceback
import logfiles
import config as cfg
import log
import time
import db_add_content as dba
from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import StandardScaler
import random
from sklearn import svm
import pickle
import os
import train_models

print("libraries loaded")

last_dataset_length = {}

def rs_to_arr(rs):
    """
    little utility function to convert a recordset with one column to an array
    :param rs:
    :return:
    """
    ret = []
    for r in rs:
        ret.append(r[0])

    return ret


def scale_data(arr):
    """

    see also here http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

    :param arr:
    :return:
    """

    #print(arr)

    scaler = StandardScaler()
    scaler.fit(arr)

    StandardScaler(copy=True, with_mean=True, with_std=True)

    #print(scaler.mean_)

    np_arr = scaler.transform(arr)

    return np_arr, scaler


def update_forgot_score(id, score):

    sql = """
    
        UPDATE vocabulary SET calc_rank =  %s WHERE id =  %s
    
    """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (score, id))
    conn.commit()
    #print("updated")
    

def predict(user_id, clf):

    """
    :param user_id:
    :param scaler:
    :return:
    """

    sql = """ 
        SELECT    
            pn_string,
            count_positive,
            count_negative,
            (CAST (count_positive AS FLOAT) /  CAST (CASE WHEN count_negative < 1 THEN 1 ELSE count_negative END  AS FLOAT)  ) as ratio,
            last_studied as age,     
            direction,
            COALESCE(count_experiments, 0) ,
            COALESCE(count_forgotten, 0),
            id
        FROM
            vocabulary
        WHERE
            user_id = %s
            and last_studied > 0
            and direction IS NOT NULL
        ORDER BY
            id
        """

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id,))

    ts_now = int(time.time())

    arr = cur.fetchall()
    arr_upgraded = []
    arr_ids = []

    for i in arr: # for each user
        #print("-------------------------------")
        r = []

        pn_string = i[0]  # pn string

        max_pos_length_ratio = 0

        if pn_string is not None:

            if len(str(pn_string)) > 0:

                if "n" in pn_string:
                    pn_arr = pn_string.split("n")

                    for s in pn_arr:
                        if "y" in s:  # to exclude words like "None"
                            ratio = len(s) / len(pn_string)  # length of yes vs. total length of string
                            if ratio > max_pos_length_ratio:
                                max_pos_length_ratio = ratio

        r.append(max_pos_length_ratio)
        r.append(i[1]) # count pos
        r.append(i[2])  # count neg
        r.append(i[3])  # ratio
        r.append(ts_now - i[4]) # age
        if i[5] == True:
            r.append(1)  # direction
        else:
            r.append(0)

        r.append(i[6])  # count experiments
        r.append(i[7])  # count forgotten

        #ensure floating pont numbers
        for x in range(len(r)):
            r[x] = float(r[x])

        arr_ids.append(i[8])
        arr_upgraded.append(r)

    arr_predict = np.asarray(arr_upgraded)

    #arr_scaled = scaler.transform(arr_predict)
    arr_scaled = arr_predict

    counter_learned = 0
    denominator_learned = 0

    for i in range(len(arr_scaled)):

        #print(X_test[i])
        one_sample = arr_scaled[i].reshape(1, -1)
        #print(one_sample)
        ret = clf.predict(one_sample)
        #print("prediction result: " + str(ret[0]))

        probability_forgot_word = ret[0]

        denominator_learned += 1
        if probability_forgot_word < 0.5:
            counter_learned += 1

    # update the percentage of learned vocabulary

    if denominator_learned > 1:
        ratio = counter_learned / denominator_learned
    else:
        ratio = 0.0

    log.log_info("user " + str(user_id) + " has a learned ratio of " + str(ratio) + " count learned = " + str(counter_learned) + " count all = " + str(denominator_learned))
    update_forgot_score(arr_ids[i], probability_forgot_word)
    update_learned_percentage(user_id, ratio)


def update_learned_percentage(user_id, ratio):

    parameter_name = "percentage_learned"

    sql = "SELECT count(*) FROM parameters WHERE user_id = %s AND key = %s"

    conn = dba.get_connection()
    cur = conn.cursor()
    #print(user_id, parameter_name, ratio)
    cur.execute(sql, (user_id, parameter_name))
    arr = cur.fetchall()

    if arr[0][0] < 1:
        # insert
        sql = "INSERT INTO parameters (user_id, key, value) VALUES (%s,%s,%s) "
        cur.execute(sql, (user_id, parameter_name, ratio))
    else:
        #update
        sql = "UPDATE parameters set value = %s WHERE user_id = %s and key = %s"
        cur.execute(sql, (ratio, user_id, parameter_name))

    conn.commit()


def boolean_to_float(arr):

    ret = []
    for i in range(len(arr)):
        if arr[i]:
            ret.append(float(1.0))
        else:
            ret.append(float(0.0))
    return ret


def train_and_predict_rs(arr, user_id, train = True):
    """
    performa  training and prediction for one user
    :param arr:
    :return:
    """

    np_arr_dirty = np.asarray(arr)

    Y = np_arr_dirty[:,0]
    X = np_arr_dirty[:,1:]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.33, random_state = 42)



    clf = train_models.train_and_choose_best(X_train, X_test, y_train, y_test)

    # save model and scaler
    # model-path
    path = cfg.parameters["model-path"]
    #print(path)

    pickle.dump(clf, open(path + str(user_id) + "-model.pickle", "wb" ))

    log.log_prediction("saved model in file system")

    #pickle.dump(scaler, open(path + str(user_id) + "-scaler.pickle", "wb" ))

    predict(user_id, clf) # predicts the forgot coefficinet for all words

    # now we predict if we forgot or not


def predict_only(user_id):

    path = cfg.parameters["model-path"]

    exists = os.path.isfile(path + str(user_id) + "-model.pickle")

    if exists:
        f = open(path + str(user_id) + "-model.pickle", "rb")
        clf = pickle.load(f)
        f.close()
        #f = open(path + str(user_id) + "-scaler.pickle", "rb")
        #scaler = pickle.load(f)

        predict(user_id, clf)


def prepare_dataset(arr):

    """

    Extract from sql recordset the values we need in the form that we need them

                success,
            pn_string,
            count_positive,
            count_negative,
            (CAST (count_positive AS FLOAT) /  CAST (CASE WHEN count_negative < 1 THEN 1 ELSE count_negative END  AS FLOAT)  ) as ratio,
            (experiment_timestamp - last_studied) as age,
            --average_pos_length,
            --max_pos_length,
            --last_pos_length,
            --pos_neg_length_ratio,
            direction,
            COALESCE(count_experiments, 0) ,
            COALESCE(count_forgotten, 0)
            --language_word,
            --language_translation,
            --word_id



    :param arr:
    :return:
    """

    ret = []

    for e in arr:

        row = []
        if e[0] == True:
            row.append(1)
        else:
            row.append(0)

        pn_string = e[1]

        max_pos_length_ratio = 0

        if "n" in pn_string:
            pn_arr = pn_string.split("n")

            for s in pn_arr:
                if "y" in s: # to exclude words like "None"
                    r = len(s) / len(pn_string)  # length of yes vs. total length of string
                    if r > max_pos_length_ratio:
                        max_pos_length_ratio = r

        row.append(max_pos_length_ratio)
        row.append(e[2]) # coutn pos
        row.append(e[3]) # count neg
        row.append(e[4]) # ratio
        row.append(e[5]) # age
        if e[6] == True:   # direction
            row.append(1)
        else:
            row.append(0)
        row.append(e[7])  # experiments
        row.append(e[8])  # num times forgotten

        # ensure floating pont numbers
        for i in range(len(row)):
            row[i] = float(row[i])

    #print(row)

        ret.append(row)

    return ret


def run_prediction_loop():

    global last_dataset_length

    sql = """ 
    
        SELECT DISTINCT
            user_id
        FROM
            history
        WHERE
            time_stamp_server > %s

        """

    time_stamp = int(time.time())

    #threshold = time_stamp - 1000
    diff = 0.1 * 60 * 60 # hours minute second
    threshold = int(time.time()) - diff

    conn = dba.get_connection()
    cur = conn.cursor()

    threshold = 0
    cur.execute(sql, (threshold,))

    user_arr = rs_to_arr(cur.fetchall())

    #print(user_arr)

    sql = """ 
        SELECT    
            success,
            pn_string,
            count_positive,
            count_negative,
            (CAST (count_positive AS FLOAT) /  CAST (CASE WHEN count_negative < 1 THEN 1 ELSE count_negative END  AS FLOAT)  ) as ratio,
            (experiment_timestamp - last_studied) as age,  
            direction,
            COALESCE(count_experiments, 0) ,
            COALESCE(count_forgotten, 0) 
        FROM
            experiments
        WHERE
            user_id = %s
            and last_studied > 0
            and success in (True, False)
            and direction IS NOT NULL
        """

    for user_id in user_arr:

        log.log_info("processing user id: " + str(user_id))

        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (user_id,))

        arr = cur.fetchall()

        log.log_info("number of data points " + str( len(arr)))

        if user_id in last_dataset_length:
            diff = len(arr) - last_dataset_length[user_id]
        else:
            diff = len(arr) - 0

        last_dataset_length[user_id] = len(arr)

        if len(arr) > 10:

            if diff > 0:
                log.log_info("running train and predict, difference is: " + str(diff))
                arr = prepare_dataset(arr)
                train_and_predict_rs(arr, user_id)
                log.log_info("train and predict done")
            else:
                # then just predict without training
                log.log_info("just predict without training because no new train data")
                predict_only(user_id)
                log.log_info("predicting done")



# -------------------------------------------------------------------

while True:

    print("running prediction")
    run_prediction_loop()
    #print("now sleeping")
    #time.sleep(60)
    time.sleep(10)