"""

ToDo make this a separate thread and the methods just put items in a queue

"""


import datetime
import time



def log_error(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("ERROR:: " + st + " :: " + str(x))


def log_info(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("INFO:: " + st + " :: " + str(x))


def log_warning(x):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("WARNING:: " + st + " :: " + str(x))
