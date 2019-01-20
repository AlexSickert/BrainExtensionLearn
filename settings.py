
import os
import pickle
import log


def get_settings(session):

    # todo: this is just a test version

    f = './test-settings.pickle'

    exists = os.path.isfile(f)

    if exists:

        pickle_in = open(f, "rb")
        data = pickle.load(pickle_in)

    else:

        data = {}
        data["Russian"] = {}
        data["Russian"]["From"] = False
        data["Russian"]["To"] = False
        data["Russian"]["Both"] = True

        data["English"] = {}
        data["English"]["From"] = False
        data["English"]["To"] = True
        data["English"]["Both"] = False

        data["Spanish"] = {}
        data["Spanish"]["From"] = True
        data["Spanish"]["To"] = False
        data["Spanish"]["Both"] = False

    return data


def set_settings(session, data):

    try:

        f = './test-settings.pickle'

        pickle_out = open(f, "wb")
        pickle.dump(data, pickle_out)
    except Exception as ex:


        log.log_error("in set_settings(session, data): " + str(ex))


