"""

is the interface to handle all requests to the slave.

getsa as an input a JSON object and sends back a json object

"""
import ssl
import socket
import config as cfg
import json



def get_from_slave(ip, port, obj):

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl.wrap_socket(listen_socket, certfile=cfg.parameters["certfile"], keyfile=cfg.parameters["keyfile"],server_side=False)
    ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("get_from_slave ", (ip, port))
    ssl_socket.connect((ip, port))

    # convert object to json string
    obj_str = json.dumps(obj)

    b = bytearray()
    b.extend(map(ord, str(len(obj_str)).zfill(10))) # tell server how long message is

    b.extend(map(ord, obj_str))

    #ssl_socket.send(b)
    ssl_socket.sendall(b)

    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = ssl_socket.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break


    data_str = "".join(map(chr, data))

    #print(data_str)

    j = json.loads(data_str)
    ssl_socket.close()

    return j

