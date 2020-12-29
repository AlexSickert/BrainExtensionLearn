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
import ssl

auth_keys = cfg.parameters["deep_l_access_token"]


def translate(source_lang, target_lang, txt_to_translate):
    """
    Entry point to the translation
    All other functions are just helper functions

    :param source_lang:
    :param target_lang:
    :param txt_to_translate:
    :return:
    """
    global auth_keys

    log.log_translation("-------- start of translation ---------")

    log.log_translation("translate(source_lang, target_lang, txt_to_translate)")

    languages = ["EN", "DE", "FR", "ES", "PT", "IT", "RU"]

    source_lang = source_lang.upper()
    target_lang = target_lang.upper()

    if source_lang not in languages:
        log.log_translation("error in translation: no source language")
        log.log_error("no source language")
        return ""

    if target_lang not in languages:
        log.log_translation("error in translation: no target language")
        log.log_error("no target language")
        return ""

    try:

        trans_exists, trans = db_add_content.get_translation(source_lang, target_lang, txt_to_translate)

        trans_exists = False

        if not trans_exists:

            success = False
            try_count = 0

            while not success:

                auth_key = auth_keys[try_count]

                try_count += 1

                log.log_translation("try counter of translate: " + str(try_count) + " of " + str(len(auth_keys)))

                if try_count >= len(auth_keys):
                    success = True # its actually not true, but we need to stop as no other option

                url = "https://api.deepl.com/v2/translate?text=" + urllib.parse.quote_plus(txt_to_translate)
                url += "&source_lang=" + source_lang
                url += "&target_lang=" + target_lang
                url += "&auth_key=" + auth_key

                log.log_translation(url)
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                resp = req.urlopen(url, context=ctx, timeout=10).read()
                res_txt = resp.decode()
                log.log_translation("------------ response json object ------------")
                log.log_translation(res_txt)
                log.log_translation("------------------------")
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

                if len(trans) > 0:
                    success = True
                    db_add_content.insert_translation(source_lang, target_lang, txt_to_translate, trans)

    except Exception as e:

        log.log_translation("error in translation: " + str(e))
        log.log_error(e)
        trans = ""

    log.log_translation("-------- end of translation ---------")

    return trans

