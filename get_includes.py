#!/usr/bin/env python

"""

this file provides the static files and includes etc. 


"""
from pathlib import Path
import log

log.log_info("loading get_includes.py")


def get_include_file_content(p):
    f = ""

    if p == "/":
        f = './html/index.html'
    if "/include/Controller.js" in p:
        f = './js/Controller.js'
    if p == "/app":
        f = './html/app.html'
    if p == "/include/DataAccess.js":
        f = './js/DataAccess.js'

    if p == "/include/UxUi.js":
        f = './js/UxUi.js'

    my_file = Path(f)

    if my_file.is_file():

        file = open(f, 'rb')
        s = file.read()
        file.close()
    else:
        log.log_info('could not find the follwing file and hence return error: ' + str(p))
        x = "error"
        s = bytearray()
        s.extend(map(ord, x))

    return s
