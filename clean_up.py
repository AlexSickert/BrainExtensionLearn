

import time
import threading
import config as cfg
import db_add_content as dba


def clean_master():

    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "DELETE FROM master_slave_mapping WHERE session_or_user like '%$testuser$%';"
    cur.execute(sql)
    conn.commit()

    print("clean up MASTER done")


def clean_slave():
    conn = dba.get_connection()
    cur = conn.cursor()
    sql = "DELETE FROM session WHERE session_string like '%$testuser$%';"
    cur.execute(sql)
    conn.commit()

    print("clean up SLAVE done")

#
# def clean_up_worker():
#
#     users_to_clean = ["user-1@data-yield.com", "user-2@data-yield.com", "monitoring@data-yield.com"]
#
#     cont = True
#
#     for x in users_to_clean:
#         print(x)
#
#     print("start doing jobs endlessly")
#
#     while cont:
#
#         print("next loop")
#         time.sleep(1)  # sleep one hour
#
#
#         #
#         # try:
#         #
#         #     for user in users_to_clean:
#         #
#         #         print(user)
#         #         #print(cfg.parameters["master-or-slave"])
#         #
#         #         if "master" in str(cfg.parameters["master-or-slave"]):
#         #
#         #             # conn = dba.get_connection()
#         #             # cur = conn.cursor()
#         #             # sql = "DELETE FROM master_slave_mapping WHERE user_email = %s;"
#         #             # cur.execute(sql, (user,))
#         #             #
#         #             # conn.commit()
#         #             #
#         #             print("done in master")
#         #
#         #         if "slave" in str(cfg.parameters["master-or-slave"]):
#         #
#         #             # this is just for slave
#         #             # this is probably not correct
#         #             # conn = dba.get_connection()
#         #             # cur = conn.cursor()
#         #             # sql ="select id from users where email = %s;"
#         #             # cur.execute(sql, (user,))
#         #             # arr = cur.fetchall()
#         #             # for row in arr:
#         #             #     id = row[0]
#         #             #     sql = "delete from session where user_id = %s;"
#         #             #     cur.execute(sql, (id,))
#         #             #     conn.commit()
#         #             print("done in slave")
#         #
#         # except Exception as ex:
#         #     print("error in clean_up()")
#         #     print("error in clean_up(): ", str(ex))
#         #
#         # print("now i go sleeping")
#         # time.sleep(1) # sleep one hour
#         #
#     print("start doing jobs endlessly end ")
#
# tc = threading.Thread(target=clean_up_worker)
# tc.setDaemon(True)
# tc.start()