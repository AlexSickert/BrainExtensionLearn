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
import report_html as reph
import legal_html as leg
import faq_html as faq
import process_get as pget
import traffic
import clean_up
import email_sender as es


es.send_mail_queued_monitoring("MASTER HTTPS application is starting", "MASTER HTTPS application is starting")


clean_up.clean_master()

log.log_info("==========================================================================")
log.log_info("==========================================================================")
log.log_info("==========================================================================")
log.log_info("------------------ start master https server ----------------------")

SERVER_ADDRESS = (HOST, PORT) = '', int(cfg.parameters["https"])
REQUEST_QUEUE_SIZE = 50

file_cache = {}


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


def getFile(path, use_cache=True):
    """
    little helper function
    :return:
    """

    global file_cache

    if use_cache:

        if path in file_cache:
            log.log_info("getFile(path) getting from cache")
            return file_cache[path]

        else:
            log.log_info("getFile(path) loading from file system")
            file = open(path, 'rb')
            s = file.read()
            file.close()
            file_cache[path] = s
            return s
    else:
        log.log_info("getFile(path) loading from file system")
        file = open(path, 'rb')
        s = file.read()
        file.close()
        file_cache[path] = s
        return s


def get_html_page(s):
    """
    it loads the html page template and fills it with the content from the file specified in s
    :param s:
    :return:
    """

    try:

        # page_template.txt

        file = open("./html/page_template.txt", 'r')
        template = file.read()
        file.close()

        file = open("./html/" + s, 'r')
        content = file.read()
        file.close()

        html = template.replace("#content#", content)
        # html += "xxx"

        html = html.encode('utf-8')

        # b = bytearray()
        # b.extend(map(ord, html))

    except Exception as ex:

        log.log_error(str(ex))
        # b = bytearray()
        # b.extend(map(ord, "Error"))

        html = "ERROR".encode('utf-8')

    return html


def getRssContent(u):
    log.log_info("in getRssContent(u) and u = " + str(u))

    txt = "nothing"

    if "rss_content_" in u:

        try:
            s = u.split("rss_content_")
            fn = s[1]
            fn = "./rss/texts/" + fn

            file = open(fn, 'r')
            txt = file.read()
            file.close()
        except Exception as ex:
            log.log_error("error opening file " + fn + " error: " + ex)
            txt = "error reading file"

    # ToDo add here needed code to make text nice and readable and right font and alos with js...

    html = """
    
        <html>
            <head>
                <meta charset="UTF-8">
            </head>
        
        
    
    """

    html += txt

    html += """
       
    </html>
    """

    # ret = bytearray()
    # ret.extend(map(ord, html.encode('utf8')))

    ret = bytearray(html, encoding="utf-8")

    return ret


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
            i += 1
            if i == 1:
                # print(l)
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


def handle_request(client_connection, ip_address, port):
    """
    This is the method that is being executed in separate threads.
    It handles the request and sends back the response.

    :param client_connection:
    :return:
    """

    print("------------------ REQUEST RECEIVED ----------------------")

    try:
        start_execution = datetime.datetime.now()
        log.log_info("------------------ REQUEST RECEIVED ----------------------")
        log.log_info("request from IP: " + ip_address)

        request = client_connection.recv(1024)
        # print(request)
        req = request.decode()

        method = ""
        form_values = {}
        elements = req.split("\r\n\r\n")

        log.log_info("get_header_values(req) ...")
        method, url, protocol, header_values, url_parameter = get_header_values(req)

        log.log_info("get_header_values(req) DONE ")

        # check if POST

        if req[:4] == "POST":
            log.log_info("it is a post request")
            method = "POST"
            # log.log_info("req: " + req)

            # print(elements)
            header = elements[0].split("\r\n")
            body = elements[1]

            # print(header)
            # print("body: " + body)

            for l in header:
                # print(l)
                fragments = l.split(":")

                # print(fragments[0])
                if "Content-Length" in fragments[0]:
                    content_length = int(fragments[1])
                    # print(content_length)

            # body lenght already retrieved
            done = len(body)
            diff = content_length - done

            log.log_info("body longer than already processed...")

            chunks = []
            if diff > 0:
                todo = diff
                while todo > 0:
                    # print(1)
                    chunk = client_connection.recv(1)
                    # print(2)
                    # print(chunk)
                    chunks.append(chunk)
                    # print(3)
                    todo -= 1

            log.log_info("adding new chunks to existing body.")
            for c in chunks:
                # print(c)
                # print(c.decode(encoding = 'UTF-8', errors = 'replace'))
                s = c.decode(encoding='UTF-8', errors='replace')
                body += s
            # print(body)
            #     log.log_info("body completely processed now.")

            form_values = handle_body(body)

        else:
            method = "GET"
            log.log_info("we are in GET")
            log.log_info(url_parameter)

        # by now we have parsed and loaded all data and can work with the input to prepare the response

        http_response = make_header()

        if "GET" in method:
            log.log_info("GET request")
            log.log_info("URL: " + url)

            # check if we need to serve a static file or process parameters
            if url.strip() == "/":
                # serve the index file
                http_response += getHtml()
            else:
                # serve other stuff
                u = url.strip()
                if u == "/app":
                    http_response += getFile("./html/app.html", False)
                elif u == "/app-android-webview":
                    http_response += getFile("./html/app-android-webview.html", False)
                elif u == "/app-ios-webview":
                    http_response += getFile("./html/app-ios-webview.html", False)
                elif u == "/rss.html":
                    http_response += getFile("./html/rss.html", False)
                elif u == "/reader.html":
                    http_response += getFile("./html/reader.html", False)
                elif "rss_content" in u:
                    http_response += getRssContent(u)
                elif u == "/Controller.js":
                    http_response += getFile("./js/Controller.js", False)
                elif u == "/Chart.js":
                    http_response += getFile("./js/Chart.js", False)
                elif u == "/UxUi.js":
                    http_response += getFile("./js/UxUi.js", False)
                elif u == "/DataAccess.js":
                    http_response += getFile("./js/DataAccess.js", False)
                elif u == "/rss.js":
                    http_response += getFile("./js/rss.js", False)
                elif u == "/ControllerReader.js":
                    http_response += getFile("./js/ControllerReader.js", False)
                elif u == "/DataAccessReader.js":
                    http_response += getFile("./js/DataAccessReader.js", False)
                elif u == "/HtmlReader.js":
                    http_response += getFile("./js/HtmlReader.js", False)
                elif u == "/Parser.js":
                    http_response += getFile("./js/Parser.js", False)
                elif u == "/UxUiReader.js":
                    http_response += getFile("./js/UxUiReader.js", False)
                elif u == "/favicon.ico":
                    http_response += getFile("./html/favicon.ico")
                elif u == "/style.css":
                    http_response += getFile("./css/style.css", False)
                elif u == "/styleReader.css":
                    http_response += getFile("./css/styleReader.css", False)
                elif u == "/rss.css":
                    http_response += getFile("./css/rss.css", False)
                elif u == "/mobile-screenshot.png":
                    http_response += getFile("./html/mobile-screenshot.png")
                elif "Screenshot_" in u:
                    u = str(u).replace("/", "")
                    u = str(u).replace("..", ".")
                    http_response += getFile("./html/" + u.strip())
                elif u == "/top-image-1.jpg":
                    http_response += getFile("./html/top-image-1.jpg")
                elif "report.html" in u:
                    http_response += reph.get_report(u)
                elif "legal.html" in u:
                    http_response += leg.get_legal()
                elif "faq.html" in u:
                    http_response += faq.get_faq()
                elif "register-slave" in u:
                    http_response += pget.process_get(header_values, url_parameter)
                elif "terms.html" in u:
                    http_response += get_html_page("terms.txt")
                elif "imprint.html" in u:
                    http_response += get_html_page("imprint.txt")
                elif "privacy.html" in u:
                    http_response += get_html_page("privacy.txt")
                elif "index" in u:
                    http_response += getHtml()
                else:
                    # handle other requests we ignore them...
                    message = "ERROR with: " + u
                    b = bytearray()
                    b.extend(map(ord, message))
                    http_response += b

        else:
            log.log_info("POST request")
            http_response = make_header()

            if header_values["content-type"].strip() == "application/json":
                # this is currently just used by the Google Spreadsheet function
                log.log_info("JSON content")
                jsonObj = parse.unquote(body)
                # message = pj.process_json(fragments, jsonObj)
                message = pj.process_json_master(jsonObj)
            else:
                # this is uded by android and web app
                message = po.process_post(form_values, ip_address)

            b = bytearray()
            b.extend(map(ord, message))
            http_response += b

        client_connection.sendall(http_response)
        client_connection.close()

        end_execution = datetime.datetime.now()
        execution_time_diff = end_execution - start_execution
        millis = execution_time_diff.total_seconds() * 1000

        log.log_info("Execution done by thread: " + str(threading.currentThread().getName()))
        log.log_info("Execution took time in milliseconds: " + str(millis))
        log.log_info("------------------- END OF REQUEST ---------------------")

    except Exception as ex:

        log.log_info("Exception in user code:" + str(ex))
        log.log_info('-' * 60)
        traceback.print_exc(file=sys.stdout)
        log.log_info('-' * 60)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # listen_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssl_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],
                                 server_side=True)

    ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_socket.bind(SERVER_ADDRESS)
    ssl_socket.listen(REQUEST_QUEUE_SIZE)

    executor = ThreadPoolExecutor(max_workers=50)

    print('MASTER Serving HTTPS on port {port} ...'.format(port=PORT))

    log.log_info('MASTER Serving HTTPS on port {port} ...'.format(port=PORT))

    while True:
        # client_connection, client_address = listen_socket.accept()
        try:
            client_connection, client_address = ssl_socket.accept()
            # log.log_info("client_user_address: " + str( client_address) )
            traffic.track(client_address[0], True)
            a = executor.submit(handle_request, client_connection, str(client_address[0]), client_address[1])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            log.log_error("Error in try-catch of main server loop: " + str(sys.exc_info()[0]))

            # new test july 2020 handling the ssl error issue

            # listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #
            # # listen_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)
            # ssl_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"],
            #                              keyfile=cfg.parameters["keyfile"],
            #                              server_side=True)
            #
            # ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # ssl_socket.bind(SERVER_ADDRESS)
            # ssl_socket.listen(REQUEST_QUEUE_SIZE)
            #
            # executor = ThreadPoolExecutor(max_workers=50)





            if "KeyboardInterrupt" in str(sys.exc_info()[0]):
                exit()


if __name__ == '__main__':
    serve_forever()
