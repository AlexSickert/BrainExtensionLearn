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


import socket
import config as cfg
from  concurrent.futures import ThreadPoolExecutor
import threading
from urllib import parse
import datetime
import process_post as po
import process_get as pg
import process_json as pj
import log
import sys, traceback
import ssl
import traffic


log.log_info("==========================================================================")
log.log_info("==========================================================================")
log.log_info("==========================================================================")
log.log_info("------------------ start http server ----------------------")

SERVER_ADDRESS = (HOST, PORT) = '', int(cfg.parameters["http"])
REQUEST_QUEUE_SIZE = 50


def getHtml():

    """
    little helper function that only loads the html code of the client
    :return:
    """

    p = "./html/index.html"
    file = open(p, 'rb')
    s = file.read()
    file.close()
    return s

def getFile(path):

    """
    little helper function
    :return:
    """

    file = open(path, 'rb')
    s = file.read()
    file.close()
    return s


def get_header_values(data):

    """
    it processes the header part of a http request. Both Post and Get
    :param data: the header data as a string
    :return: it returns several paramters: method, url, protocol, header_values, url_parameter.

    header_values are the Header data such as Cookie

    url_parameter is a dictionary with key value pairs extracted from the URL like /?a=1&b=2


    """

    log.log_info("data has length: " + str(len(data)))


    method = ""
    url = ""
    protocol = ""
    header_values = {}
    url_parameter = {}



    lines = data.split("\r\n")

    i = 0
    for l in lines:
        if len(l) > 0:
            log.log_info("current line: " + str(l))
            i += 1
            if i == 1:
                print(l)
                log.log_info("first line string: " + str(l))
                try:
                    method, url, protocol = l.split(" ")
                except:
                    print("Error in first line:", sys.exc_info()[0])
                    log.log_error("Error in first line: " + str(sys.exc_info()[0]))
                    log.log_info("Error in first line. Line content was: " + str(l))
                    method = ""
                    url = "/"
                    protocol = ""

            else:
                pos = l.find(":")
                # we make the header values all lower case to reduce one source of error

                k = l[:pos]
                k = k.strip().lower()
                header_values[k] = l[pos + 2:]

    if "?" in url:

        parts = url.split("?")
        if "&" in parts[1]:
            chunks = parts[1].split("&")
            for c in chunks:
                k, v = c.split("=")
                url_parameter[k] = parse.unquote(v)
        else:
            k, v = parts[1].split("=")
            url_parameter[k] = parse.unquote(v)

    return method, url, protocol, header_values, url_parameter


def handle_body(s):

    """
    This function takes the body of a request as an input and extracts the parameters
    it returns a dictionary
    :param s: body part of a http POST request
    :return: dictionary with key value pairs where the key is the form parameter
    """

    values = {}

    if "&" in s:
        chunks = s.split("&")

        for c in chunks:
            if "=" in c:
                k, v = c.split("=")
                values[k] = parse.unquote(v)

    else:
        if "=" in s:
            k, v = s.split("=")
            # log.log_info(k)
            # log.log_info(v)
            # log.log_info(parse.unquote(v))
            values[k] = parse.unquote(v)

    return values

def make_header():

    """
    DO NOT CHANGE THIS WEIRD FORMATTING. IT HAS TO BE LIKE THAT
    :return:
    """

    http_response = b"""\
HTTP/1.1 200 OK

"""

    return http_response


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

        request = client_connection.recv(1024)
        # print(request)
        req = request.decode()

        method = ""
        form_values = {}
        elements = req.split("\r\n\r\n")

        log.log_info("get_header_values(req) ...")
        method, url, protocol, header_values, url_parameter = get_header_values(req)

        log_str = str(method) + "|" + str(url) + "|" + str(protocol) + "|" + str(url_parameter) + "|" + str(header_values)
        log.log_info(log_str)

        log.log_info("get_header_values(req) DONE ")

        http_response = make_header()
        http_response += getFile("./html/redirect.html")

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
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)

    executor = ThreadPoolExecutor(max_workers=50)

    log.log_info('Serving HTTP on port {port} ...'.format(port=PORT))

    while True:
        #client_connection, client_address = listen_socket.accept()
        try:
            # client_connection, client_address = ssl_socket.accept()
            client_connection, client_address = listen_socket.accept()
            traffic.track(client_address[0], False)
            a = executor.submit(handle_request, client_connection)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            log.log_error("Error in try-catch of main server loop: " + str(sys.exc_info()[0]))



if __name__ == '__main__':
    serve_forever()