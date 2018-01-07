
import datetime
import socket

from  concurrent.futures import ThreadPoolExecutor
import threading
from urllib import parse
import log


SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def getHtml():

    p = "./client.html"
    file = open(p, 'rb')
    s = file.read()
    file.close()
    return s


def get_header_and_body(data):

    method = ""
    url = ""
    protocol = ""
    header_values = {}
    header = True
    body = ""
    body_values = {}


    lines = data.split("\n")
    i = 0
    for l in lines:
        l = l.replace("\r", "")
        i += 1
        if header:
            if i == 1:
                method, url, protocol = l.split(" ")

            else:
                pos = l.find(":")
                header_values[l[:pos]] = l[pos + 2:]

            if len(l.strip()) < 1:
                header = False
        else:
            # now we are in the body
            body += l

    body_values = handle_body(body)

    return method, url, protocol, header_values, body_values


def handle_body(s):

    values = {}

    if "&" in s:
        chunks = s.split("&")

        for c in chunks:
            if "=" in c:
                k, v = c.split("=")
                values[k] = parse.unquote(v)

    else:
        if "=" in s:
            #print("splitting")
            k, v = s.split("=")
            print(k)
            print(v)
            print(parse.unquote(v))
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

    start_execution = datetime.datetime.now()

    log.log_info("------------------ start GET ----------------------")


    request = client_connection.recv(1024)



    req = request.decode()
    print(req)

    method, url, protocol, header_values, body = get_header_and_body(req)


    if "GET" in method:



        print("GET request")

        http_response = make_header()
        http_response += getHtml()

    else:
        #print("POST request")

        http_response = make_header()

        #method, url, protocol, header_values, body = get_header_and_body(req)

        print(body)

        message = threading.currentThread().getName()

        message += " aslkdjf ;laksjd f;lajs df;lkjas d;lfkj a;sdlkfj "


        b = bytearray()
        b.extend(map(ord, message))

        http_response += b


    # print(http_response)
    client_connection.sendall(http_response)
    client_connection.close()

    end_execution = datetime.datetime.now()
    execution_time_diff = end_execution - start_execution
    millis = execution_time_diff.total_seconds() * 1000
    log.log_info("Execution took time in milliseconds: " + str(millis))
    log.log_info("-------------------end GET ---------------------")


def serve_forever():

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)

    executor = ThreadPoolExecutor(max_workers=15)

    print('Serving HTTP on port {port} ...'.format(port=PORT))

    while True:
        client_connection, client_address = listen_socket.accept()
        a = executor.submit(handle_request, client_connection)

if __name__ == '__main__':
    serve_forever()