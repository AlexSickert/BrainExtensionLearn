"""

Functions to monitor traffic
- Where traffic comes from
- Who is calling the application how frequently

We use a separate thread to handle the requests so that it has no impact on the overall app

"""

import queue
import time
import threading
import db_security
import urllib.request as req
import json
import config as cfg


ip_2_location_cache = {}
ip_last_request_timestamp = {}
time_stamp_last_call = 0
traffic_q = queue.Queue()


def track(ip_address, is_https):

    global traffic_q

    ts = time.time()

    item = []
    item.append(ip_address)
    item.append(ts)
    item.append(is_https)
    traffic_q.put(item)


def get_location_from_service(ip):
    """
    check this https://ipstack.com/documentation

    https://api.ipstack.com/134.201.250.155 ? access_key = YOUR_ACCESS_KEY

    http://api.ipstack.com/212.90.63.230?access_key=0f081e5722cb3004ca98ea8fce2d8ce8
    ipstack_access_key

    :param ip:
    :return:
    """
    try:
        url = "http://api.ipstack.com/" + str(ip).strip() + "?access_key=" + cfg.parameters["ipstack_access_key"]
        resp = req.urlopen(url, timeout=10).read()
        return resp.decode()
    except Exception as e:
        print(str(e))
        return "error"


def get_location(ip_address):

    global ip_2_location_cache

    if ip_address in ip_2_location_cache:
        return ip_2_location_cache[ip_address]

    else:

        loc = get_location_from_service(ip_address)
        ip_2_location_cache[ip_address] = loc
        return loc


def traffic_worker():

    global traffic_q
    global ip_2_location_cache
    global ip_last_request_timestamp
    global time_stamp_last_call

    while True:

        if traffic_q.qsize() > 0:
            item = traffic_q.get()

            if item is not None:
                try:

                    # this writes it to the log file created by bash
                    print(item[1])

                    ip = item[0]
                    ts = item[1]

                    # process time stamps
                    if ip in ip_last_request_timestamp:
                        delta_this_ip = ts - int(ip_last_request_timestamp[ip])
                    else:
                        delta_this_ip = ts

                    delta_all = ts - time_stamp_last_call

                    db_security.insert_into_db(ip, ts, delta_all, delta_this_ip, item[2])

                    ip_last_request_timestamp[ip] = ts
                    time_stamp_last_call = ts


                    # insert location
                    loc = get_location(ip)
                    db_security.insert_ip_loction(ip, ts, loc)


                    traffic_q.task_done()

                except Exception as ex:
                    print("error in export  traffic_worker()")
                    print("error in export  traffic_worker(): ", str(ex))
        else:
            time.sleep(1)


t = threading.Thread(target=traffic_worker)
t.setDaemon(True)
t.start()


