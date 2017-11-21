#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

from     https://gist.github.com/bradmontgomery/2219997

reading from socket https://stackoverflow.com/questions/822001/python-sockets-buffering 

base http server https://wiki.python.org/moin/BaseHttpServer 

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import get_includes as gi
import process_post as po


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')

        self.send_header('Set-Cookie', 'B=412341234')

        self.end_headers()

    def do_GET(self):
        print("------------------ start GET ----------------------")

        self._set_headers()
        p = self.path

        print(self.path)
        print(self.headers)

        s = gi.get_include_file_content(p)

        # now write response
        self.wfile.write(s)

        print("-------------------end GET ---------------------")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        print("------------- start POST ------------------")
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself


        print(post_data)
        # process post data and make response
        ret = po.process_post(post_data)

        # write response
        self._set_headers()
        self.wfile.write(ret.encode())

        print("-------------- end POST --------------------------")


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
