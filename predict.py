"""

This script runs the prediction. It is the central point of the application in the sense that everythng else is
more or less just infrastructure. Here is the magic point where we predict which workd will be forgotten soon.


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
    

def predict(user_id, scaler, clf):

    """
    :param user_id:
    :param scaler:
    :return:
    """

    sql = """ 
        SELECT    
            count_positive,
            count_negative,
            (CAST (count_positive AS FLOAT) /  CAST (CASE WHEN count_negative < 1 THEN 1 ELSE count_negative END  AS FLOAT)  ) as ratio,
            last_studied as age,     
            direction,
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

    for i in range(len(arr)):
        r = []
        for x in range(5):
            if x == 3:
                r.append(ts_now - arr[i][x])
            else:
                r.append(arr[i][x])
        arr_ids.append(arr[i][5])
        arr_upgraded.append(r)

    arr_predict = np.asarray(arr_upgraded)

    arr_scaled = scaler.transform(arr_predict)

    for i in range(len(arr_scaled)):

        #print(X_test[i])
        one_sample = arr_scaled[i].reshape(1, -1)
        ret = clf.predict(one_sample)
        #print("id: ", arr_ids[i])
        #print(ret[0])

        pro = clf.predict_proba(one_sample)



        #if ret[0] < 1.0:
        print("classes: ", clf.classes_, " id: ", arr_ids[i], " result: ", ret, " forgotten: ", pro[0][0] , " learned: ", pro[0][1] )

        probability_forgot_word = pro[0][0]

        update_forgot_score(arr_ids[i], probability_forgot_word)


def boolean_to_float(arr):

    ret = []
    for i in range(len(arr)):
        if arr[i]:
            ret.append(float(1.0))
        else:
            ret.append(float(0.0))
    return ret


def train_and_predict_rs(arr, user_id):
    """
    performa  training and prediction for one user
    :param arr:
    :return:
    """

    np_arr_dirty = np.asarray(arr)



    Y = np_arr_dirty[:,0]
    X = np_arr_dirty[:,1:]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.33, random_state = 42)

    y_train = boolean_to_float(y_train)
    y_test = boolean_to_float(y_test)

    X_train, scaler = scale_data(X_train)
    X_test = scaler.transform(X_test)

    print(X_train)
    #print(X_test)
    print(y_train)
    #print(y_test)

    #clf = tree.DecisionTreeClassifier()
    clf = svm.SVC(gamma='auto', probability=True)

    #X_train = X_train.astype(float)

    clf = clf.fit(X_train, y_train)

    c_total = 0
    c_pos = 0

    for i in range(len(X_test)):

        #print(X_test[i])
        one_sample = X_test[i].reshape(1, -1)
        ret = clf.predict(one_sample)
        pro = clf.predict_proba(one_sample)
        #print("result: ", ret , " forgot_probab: ", pro[0][0])

        probability_forgot_word = pro[0][0]


        truth = y_test[i]
        #print("truth: ", truth)
        c_total += 1

        if ret[0] == truth:
            c_pos += 1

    print("score: ", c_pos / c_total)

    #print(clf.feature_importances_)

    predict(user_id, scaler, clf)

    # now we predict if we forgot or not


def run_prediction_loop():
    sql = "SELECT DISTINCT user_id FROM experiments"

    conn = dba.get_connection()
    cur = conn.cursor()
    cur.execute(sql, ())

    user_arr = rs_to_arr(cur.fetchall())

    # print(user_arr)

    sql = """ 
        SELECT    
            success,
            --pn_string,
            count_positive,
            count_negative,
            (CAST (count_positive AS FLOAT) /  CAST (CASE WHEN count_negative < 1 THEN 1 ELSE count_negative END  AS FLOAT)  ) as ratio,
            (experiment_timestamp - last_studied) as age,
            --average_pos_length,
            --max_pos_length,
            --last_pos_length,
            --pos_neg_length_ratio,      
            direction
            --language_word,
            --language_translation,  
            --word_id
                
        FROM
            experiments
        WHERE
            user_id = %s
            and last_studied > 0
            and success in (True, False)
            and direction IS NOT NULL
        """

    for user_id in user_arr:

        print("----------------------------------------------------------------------------------------------------")

        print("processing user ", user_id)

        conn = dba.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (user_id,))

        arr = cur.fetchall()

        print("number of data points ", len(arr))

        if len(arr) > 10:
            train_and_predict_rs(arr, user_id)


# -------------------------------------------------------------------

while True:

    run_prediction_loop()
    print("now sleeping")
    time.sleep(60)