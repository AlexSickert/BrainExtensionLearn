"""

simple translation service that calls DEEPL API and caches the word

"""

import queue
import time
import threading
import db_security
import urllib.request as req
import json
import config as cfg
import db_add_content
import log
import urllib.parse

auth_key = cfg.parameters["deep_l_access_token"]


def translate(source_lang, target_lang, txt_to_translate):
    """
    Entry point to the translation
    All other functions are just helper functions

    :param source_lang:
    :param target_lang:
    :param txt_to_translate:
    :return:
    """
    global auth_key

    log.log_info("translate(source_lang, target_lang, txt_to_translate)")

    languages = ["EN", "DE", "FR", "ES", "PT", "IT", "RU"]

    source_lang = source_lang.upper()
    target_lang = target_lang.upper()

    if source_lang not in languages:
        return ""

    if target_lang not in languages:
        return ""

    try:

        trans_exists, trans = db_add_content.get_translation(source_lang, target_lang, txt_to_translate)

        trans_exists = False

        if not trans_exists:

            url = "https://api.deepl.com/v2/translate?text=" + urllib.parse.quote_plus(txt_to_translate)
            url += "&source_lang=" + source_lang
            url += "&target_lang=" + target_lang
            url += "&auth_key=" + auth_key
            print(url)
            log.log_info(url)
            resp = req.urlopen(url, timeout=10).read()
            res_txt = resp.decode()
            log.log_info(res_txt)
            res_obj = json.loads(res_txt)

            trans = ""
            counter = 0

            if "translations" in res_obj:
                for t in res_obj["translations"]:
                    if "text" in t:
                        if counter > 0:
                            trans += " | "
                        trans += t["text"]
                        counter += 1

            print("result: ")
            print("trans")
            db_add_content.insert_translation(source_lang, target_lang, txt_to_translate, trans)
            print("insterted in db")

    except Exception as e:

        log.log_info(e)
        trans = ""

    return trans

