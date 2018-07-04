"""

Collection of functions to verify session and logins


"""

import db_security as dbs


def check_login(user, password):

    ret = dbs.check_login(user, password)

    if ret > 0:
        return True
    else:
        return False


def get_user_id(user):

    return dbs.get_user_id(user)

