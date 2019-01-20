
import db_security as dbc

def process_get(header_parameters, url_parameters):

    if "security-key" in url_parameters:

        if url_parameters["security-key"] == "YI64QZ8LMPJET0GV4CCV":

            print("slave id is: ", url_parameters["slave-id"])

            slave_id = url_parameters["slave-id"]

            if "register-session" in url_parameters:

                print("need to register session", url_parameters["register-session"])

                session = url_parameters["register-session"]

                dbc.register_slave(session, slave_id)

            if "register-user" in url_parameters:

                print("need to register user", url_parameters["register-user"])
                user = url_parameters["register-user"]
                dbc.register_slave(user, slave_id)

    message = "all good"
    b = bytearray()
    b.extend(map(ord, message))

    return b