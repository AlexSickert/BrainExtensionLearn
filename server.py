import socket

from  concurrent.futures import ThreadPoolExecutor
import threading
from urllib import parse
import datetime
import process_post as po
import process_get as pg
import log

log.log_info("------------------ start server ----------------------")

SERVER_ADDRESS = (HOST, PORT) = '', 8888
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

    print("data has length: " + str(len(data)))

    print("++++++++++++++++++++++++++++++++")
    print(data)
    print("++++++++++++++++++++++++++++++++")

    method = ""
    url = ""
    protocol = ""
    header_values = {}
    url_parameter = {}


    lines = data.split("\r\n")
    i = 0
    for l in lines:
        i += 1
        if i == 1:
            method, url, protocol = l.split(" ")

        else:
            pos = l.find(":")
            header_values[l[:pos]] = l[pos + 2:]


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

    """
    This is the method that is being executed in separate threads.
    It handles the request and sends back the response.

    :param client_connection:
    :return:
    """

    start_execution = datetime.datetime.now()
    print("---------------------------------------------------------")

    request = client_connection.recv(1024)
    print(request)
    req = request.decode()

    method = ""
    form_values = {}
    elements = req.split("\r\n\r\n")
    method, url, protocol, header_values, url_parameter = get_header_values(req)



    #check if POST

    if req[:4] == "POST":
        print("it is a post request")
        method = "POST"
        print("req: " + req)

        print("------" )
        # print(elements)
        header = elements[0].split("\r\n")
        body = elements[1]

        # print(header)
        # print("body: " + body)

        for l in header:
            print(l)
            fragments = l.split(":")

            # print(fragments[0])
            if "Content-Length" in fragments[0]:
                content_length = int(fragments[1])
                # print(content_length)

        #body lenght already retrieved
        done = len(body)
        diff = content_length - done

        chunks = []
        if diff > 0:
            todo = diff
            while todo > 0:

                chunk = client_connection.recv(1)
                chunks.append(chunk)
                todo -= 1

        for c in chunks:
            s = c.decode()
            body += s
        # print(body)
        print("asdfasdfasdfasdfasdfasdf")
        form_values = handle_body(body)

    else:
        method = "GET"
        print("we are in GET")
        print(url_parameter)

    # by now we have parsed and loaded all data and can work with the input to prepare the response

    http_response = make_header()

    if "GET" in method:
        print("GET request")
        print("URL: " + url)


        # check if we need to serve a static file or process parameters
        if url.strip() == "/":
            # serve the index file
            http_response += getHtml()
        else:
            # serve other stuff
            u = url.strip()
            if u == "/app":
                http_response += getFile("./html/app.html")
            elif u == "/Controller.js":
                http_response += getFile("./js/Controller.js")
            elif u == "/UxUi.js":
                http_response += getFile("./js/UxUi.js")
            elif u == "/DataAccess.js":
                http_response += getFile("./js/DataAccess.js")
            else:
                # handle other requests
                message = pg.process_get(fragments, url_parameter)
                b = bytearray()
                b.extend(map(ord, message))
                http_response += b

    else:
        print("POST request")
        http_response = make_header()
        message = po.process_post(fragments, form_values)
        b = bytearray()
        b.extend(map(ord, message))
        http_response += b

    client_connection.sendall(http_response)
    client_connection.close()

    end_execution = datetime.datetime.now()
    execution_time_diff = end_execution - start_execution
    millis = execution_time_diff.total_seconds() * 1000

    print("Execution done by thread: " + str(threading.currentThread().getName()))
    print("Execution took time in milliseconds: " + str(millis))
    print("-------------------end GET ---------------------")


def serve_forever():

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)

    executor = ThreadPoolExecutor(max_workers=50)

    print('Serving HTTP on port {port} ...'.format(port=PORT))

    while True:
        client_connection, client_address = listen_socket.accept()
        a = executor.submit(handle_request, client_connection)

if __name__ == '__main__':
    serve_forever()