"""

ToDo make this a separate thread and the methods just put items in a queue

"""


import datetime
import time
import queue
import threading
import config as cfg
from  datetime import date

log_q = queue.Queue()

log_path = cfg.parameters["log-path"]


def log_error(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    s = "ERROR:: " + st + " :: " + str(x)
    #print(s)

    item = []
    item.append("e")
    item.append(s)
    log_q.put(item)

def log_prediction(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S;')
    s = st + ";" + str(x)
    #print(s)

    item = []
    item.append("p")
    item.append(s)
    log_q.put(item)


def log_ip_2_location(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S;')
    s = st + ";" + str(x)
    #print(s)

    item = []
    item.append("i")
    item.append(s)
    log_q.put(item)

def log_info(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    s = "INFO:: " + st + " :: " + str(x)
    #print(s)

    item = []
    item.append("i")
    item.append(s)
    log_q.put(item)


def log_warning(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    s = "WARNING:: " + st + " :: " + str(x)

    #print(s)

    item = []
    item.append("w")
    item.append(s)
    log_q.put(item)


def write_to_file(s, suffix=""):

    global log_path

    try:
        #print(s)
        d = date.today()
        if len(suffix) > 0:
            f = open(log_path + suffix + "-" + str(d) + ".log", "a+")
        else:
            f = open(log_path + "BrainExtension-" + str(d) + ".log", "a+")
        f.write(s + "\r\n")
        f.close()
    except Exception as ex:
        print("could not print in logger", ex)


def log_worker():
    """
    This is an endless loop that checks if there are items in the queue and if yes, we process the item and move to the
    next one. If no items in queue, then we sleep for a while.
    :return:
    """

    global log_q
    while True:

        if log_q.qsize() > 0:
            item = log_q.get()

            if item is not None:
                try:

                    # this writes it to the log file created by bash
                    print(item[1])

                    # write to general log file
                    write_to_file(item[1], suffix="")

                    if item[0] == "e":
                        write_to_file(item[1], suffix="ERROR")

                    if item[0] == "p":
                        write_to_file(item[1], suffix="PREDICTION")
                    if item[0] == "i":
                        write_to_file(item[1], suffix="IP-2-LOCATION")

                    log_q.task_done()
                except Exception as ex:
                    print("error in export  worker()")
                    print("error in export  worker(): ", str(ex))
        else:
            time.sleep(1)


t = threading.Thread(target=log_worker)
t.setDaemon(True)
t.start()
