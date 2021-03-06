"""

This pice of code is the entry point of the application and constitutes a multi threaded server. The basic logic
of the server is this:

1. accept a connection request
2. read the header
3. if the header indicates a get request, then the header is enough to read. Process the GET request. This also includes
   request to stream a static file from the file system to the client.
4. if the header indicates a POST request, then continue reading from the socket as many bites as indicated in
   the header.
5. within the POST requests distinguish if the body is a JSON object or not. Depending on this process the request
   further.


"""

import sys


import socket
import config as cfg
from  concurrent.futures import ThreadPoolExecutor
import threading
from urllib import parse
import datetime
import process_post as po
import process_get as pg

import log
import traceback
import ssl
import report_html as reph
import legal_html as leg
import faq_html as faq
import json
import process_json as pj
import clean_up
import re
import email_sender as es

log.log_info("------------------ start server ----------------------")

es.send_mail_queued_monitoring("SLAVE application is starting", "application is starting")

clean_up.clean_slave()



invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)



# use command line argument to choose server identiy
if len(sys.argv) > 1:
    server_id = sys.argv[1]
else:
    print("server ID missing. No commandline argument. Shutting down")
    exit(1)

cfg.slave_id = server_id
port = int(cfg.slaves[server_id][1])
print("server listening to port", port)
SERVER_ADDRESS = (HOST, PORT) = '', port
REQUEST_QUEUE_SIZE = 50

# we first need to ensure that the slave_id is set - therefore we can run this line only here
clean_up.re_register_at_master()


def distribute_actions(jo):

    ret_str = "error"

    if "action" in jo:
        ret_str = pj.distribute_actions(jo)

        # cfg.slave_id
    else:
        # google spreadsheed uses "function"
        f = jo["function"]

        if f == 'upload_google_spreadsheet':
            ret_str = pj.process_json(jo)


    return ret_str


def handle_request(client_connection):

    """
    This is the method that is being executed in separate threads.
    It handles the request and sends back the response.

    :param client_connection:
    :return:
    """

    try:
        start_execution = datetime.datetime.now()
        log.log_info("------------------ REQUEST RECEIVED ----------------------")

        # load 10 characters and convert to number
        request = client_connection.recv(10)
        #client_connection.
        print(request)
        req = request.decode()
        print("...")
        print(req)
        print("...")
        #print(int(req))

        todo = int(req)

        #request = client_connection.recv(int(req))
        #obj_str = request.decode()
        #obj_str = request.decode('utf-8', errors='ignore')

        chunks = []

        if todo > 0:
            while todo > 0:
                chunk = client_connection.recv(1)
                chunks.append(chunk)
                todo -= 1

        obj_str = ""
        for c in chunks:
            s = c.decode(encoding='UTF-8', errors='replace')
            obj_str += s




        #jo = json.loads(repair(obj_str))
        jo = json.loads(obj_str)

        # try:
        #     jo = json.loads(obj_str)
        # except Exception as ex:


        # the next line throws and error when object contains cyrillic. So don't uncomment!
        #print(jo)

        ret_str = distribute_actions(jo)

        #j = {}
        #j["m"] = "hello master Гаджеты для Пентаго i am slave ;lksdjf as dj f;lkasjd f;lkjas d;lfkj a;sdlkfj "
        #message = json.dumps(j)

        message = ret_str

        #http_response = b""""""

        b = bytearray()
        b.extend(map(ord, message))
        http_response = b

        client_connection.sendall(http_response)
        client_connection.close()

        end_execution = datetime.datetime.now()
        execution_time_diff = end_execution - start_execution
        millis = execution_time_diff.total_seconds() * 1000

        log.log_info("Execution done by thread: " + str(threading.currentThread().getName()))
        log.log_info("Execution took time in milliseconds: " + str(millis))
        log.log_info("------------------- END OF REQUEST ---------------------")

    except:

        log.log_info("Exception in user code:")
        log.log_info('-' * 60)
        traceback.print_exc(file=sys.stdout)
        log.log_info('-' * 60)


def serve_forever():

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    #listen_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssl_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],server_side=True)

    ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_socket.bind(SERVER_ADDRESS)
    ssl_socket.listen(REQUEST_QUEUE_SIZE)

    executor = ThreadPoolExecutor(max_workers=10)

    log.log_info('SLAVE Serving HTTP on port {port} ...'.format(port=PORT))

    while True:
        #client_connection, client_address = listen_socket.accept()
        try:
            client_connection, client_address = ssl_socket.accept()
            log.log_info("client_user_address: " + str( client_address) )
            a = executor.submit(handle_request, client_connection)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            log.log_error("Error in try-catch of main server loop: " + str(sys.exc_info()[0]))



            if "KeyboardInterrupt" in str(sys.exc_info()[0]):
                exit()



if __name__ == '__main__':
    serve_forever()