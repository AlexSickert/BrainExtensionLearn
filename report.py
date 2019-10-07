import db_report
import time
import db_add_content as dba
import datetime
import time

daily_percentage_update = {}


def get_clicks_last_24_hours(user_id):

    time_stamp_now = int(time.time())
    diff = 24 * 60 * 60
    time_stamp_start = time_stamp_now - diff

    sql = """
    
    SELECT
    
        count(time_stamp_server)
    
    FROM
        history
    WHERE
        time_stamp_server >= %s
    AND
        time_stamp_server <= %s 
    
    """

    conn = dba.get_connection()
    cur = conn.cursor()

    cur.execute(sql, (time_stamp_start, time_stamp_now))

    arr = rs_to_arr(cur.fetchall())
    return arr[0]


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


sql = """ 

    SELECT DISTINCT
        user_id
    FROM
        history
    WHERE
        time_stamp_server > %s

    """


conn = dba.get_connection()
cur = conn.cursor()

threshold = 0
cur.execute(sql, (threshold,))

user_arr = rs_to_arr(cur.fetchall())

for user_id in user_arr:

    id = str(user_id) + "-" + str(datetime.date.today())

    if not id in daily_percentage_update:

        new_words, learned_words, ratio_learned = db_report.get_simple_report(user_id)

        db_report.add_to_progress(user_id,1,ratio_learned)
        db_report.add_to_progress(user_id, 2, new_words)
        db_report.add_to_progress(user_id, 3, learned_words)
        db_report.add_to_progress(user_id, 4, get_clicks_last_24_hours(user_id))

        get_clicks_last_24_hours(user_id)

        # extract click last 24 hours

        daily_percentage_update[id] = True