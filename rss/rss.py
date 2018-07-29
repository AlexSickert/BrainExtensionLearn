
import xml.etree.ElementTree as ET
import urllib.request  as req
import re
import random
import json
import os.path
import pickle
from time import gmtime, strftime


db = []

def get_dictionary(name):

    #print("get dictionary: " + name)

    file_name = name + ".pickle"

    if os.path.isfile(file_name):
        fileObject = open(file_name, 'rb')
        # load the object from the file into var b
        ret = pickle.load(fileObject)
    else:
        d = {}
        fileObject = open(file_name, 'wb')
        pickle.dump(d, fileObject)
        ret = d
    return ret

def save_dictionary(name, data):
    file_name = name + ".pickle"
    fileObject = open(file_name, 'wb')
    pickle.dump(data, fileObject)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def handle_one_text(language, txt):

    dic = get_dictionary(language)

    arr = txt.split()

    for word in arr:

        word_clean = word.strip()

        if len(word_clean) > 0:

            if not hasNumbers(word_clean):

                if word_clean in dic:
                    dic[word_clean] += 1
                else:
                    dic[word_clean] = 1

    #now save the dictionary
    save_dictionary(language, dic)

def check_if_url_done(url):

    dic = get_dictionary("URLs")

    if url in dic:
        #print("url already done: " + url)
        return True
    else:
        return False

def set_url_done(url):

    dic = get_dictionary("URLs")
    dic[url] = True
    save_dictionary("URLs", dic)


def wrap_link(txt, lnk):

    ret = "<a href='"
    ret += lnk
    ret += "' ratget='_blank'>"
    ret += txt
    ret += "</a>"
    return ret


def html_2_text(html):

    spacer = "8Sh6Sw5Wb4Ee9Mi2Rd2R"

    txt = str(html) + " "

    txt = txt.replace("<p", spacer + "<p")
    txt = txt.replace("<div", spacer + "<div")

    txt = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", txt)
    txt = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", txt)
    txt = re.sub(r"<.+?>", " ", txt)

    txt = re.sub(r",", " ", txt)
    # txt = re.sub(r""", " ", txt)
    txt = re.sub(r"»", " ", txt)
    txt = re.sub(r"«", " ", txt)
    txt = re.sub(r"\.", " ", txt)
    txt = re.sub(r":", " ", txt)
    txt = re.sub(r"#", " ", txt)
    txt = re.sub(r"=", " ", txt)
    txt = re.sub(r"\(", " ", txt)
    txt = re.sub(r"\)", " ", txt)
    txt = re.sub(r"\[", " ", txt)
    txt = re.sub(r"\]", " ", txt)
    txt = re.sub(r"\n", " ", txt)
    #txt = re.sub(r""", " ", txt)
    txt = re.sub(r"&rsquo;", "'", txt)
    txt = re.sub(r"&raquo;", " ", txt)
    txt = re.sub(r"&laquo;", " ", txt)
    txt = re.sub(r"&Agrave;", "À", txt)
    txt = re.sub(r"&Aacute;", "Á", txt)
    txt = re.sub(r"&Acirc;", "Â", txt)
    txt = re.sub(r"&Atilde;", "Ã", txt)
    txt = re.sub(r"&Auml;", "Ä", txt)
    txt = re.sub(r"&Aring;", "Å", txt)
    txt = re.sub(r"&AElig;", "Æ", txt)
    txt = re.sub(r"&Ccedil;", "Ç", txt)
    txt = re.sub(r"&Egrave;", "È", txt)
    txt = re.sub(r"&Eacute;", "É", txt)
    txt = re.sub(r"&Ecirc;", "Ê", txt)
    txt = re.sub(r"&Euml;", "Ë", txt)
    txt = re.sub(r"&Igrave;", "Ì", txt)
    txt = re.sub(r"&Iacute;", "Í", txt)
    txt = re.sub(r"&Icirc;", "Î", txt)
    txt = re.sub(r"&Iuml;", "Ï", txt)
    txt = re.sub(r"&ETH;", "Ð", txt)
    txt = re.sub(r"&Ntilde;", "Ñ", txt)
    txt = re.sub(r"&Ograve;", "Ò", txt)
    txt = re.sub(r"&Oacute;", "Ó", txt)
    txt = re.sub(r"&Ocirc;", "Ô", txt)
    txt = re.sub(r"&Otilde;", "Õ", txt)
    txt = re.sub(r"&Ouml;", "Ö", txt)
    txt = re.sub(r"&times;", "×", txt)
    txt = re.sub(r"&Oslash;", "Ø", txt)
    txt = re.sub(r"&Ugrave;", "Ù", txt)
    txt = re.sub(r"&Uacute;", "Ú", txt)
    txt = re.sub(r"&Ucirc;", "Û", txt)
    txt = re.sub(r"&Uuml;", "Ü", txt)
    txt = re.sub(r"&Yacute;", "Ý", txt)
    txt = re.sub(r"&THORN;", "Þ", txt)
    txt = re.sub(r"&szlig;", "ß", txt)
    txt = re.sub(r"&agrave;", "à", txt)
    txt = re.sub(r"&aacute;", "á", txt)
    txt = re.sub(r"&acirc;", "â", txt)
    txt = re.sub(r"&atilde;", "ã", txt)
    txt = re.sub(r"&auml;", "ä", txt)
    txt = re.sub(r"&aring;", "å", txt)
    txt = re.sub(r"&aelig;", "æ", txt)
    txt = re.sub(r"&ccedil;", "ç", txt)
    txt = re.sub(r"&egrave;", "è", txt)
    txt = re.sub(r"&eacute;", "é", txt)
    txt = re.sub(r"&ecirc;", "ê", txt)
    txt = re.sub(r"&euml;", "ë", txt)
    txt = re.sub(r"&igrave;", "ì", txt)
    txt = re.sub(r"&iacute;", "í", txt)
    txt = re.sub(r"&icirc;", "î", txt)
    txt = re.sub(r"&iuml;", "ï", txt)
    txt = re.sub(r"&eth;", "ð", txt)
    txt = re.sub(r"&ntilde;", "ñ", txt)
    txt = re.sub(r"&ograve;", "ò", txt)
    txt = re.sub(r"&oacute;", "ó", txt)
    txt = re.sub(r"&ocirc;", "ô", txt)
    txt = re.sub(r"&otilde;", "õ", txt)
    txt = re.sub(r"&ouml;", "ö", txt)
    txt = re.sub(r"&divide;", "÷", txt)
    txt = re.sub(r"&oslash;", "ø", txt)
    txt = re.sub(r"&ugrave;", "ù", txt)
    txt = re.sub(r"&uacute;", "ú", txt)
    txt = re.sub(r"&ucirc;", "û", txt)
    txt = re.sub(r"&uuml;", "ü", txt)
    txt = re.sub(r"&yacute;", "ý", txt)
    txt = re.sub(r"&thorn;", "þ", txt)
    txt = re.sub(r"&yuml;", "ÿ", txt)
    txt = re.sub(r"&nbsp;", " ", txt)
    txt = re.sub(r"&#9642;", "", txt)  # black small square

    txt = txt.replace("!", " ")
    txt = txt.replace("?", " ")
    txt = txt.replace("<", " ")
    txt = txt.replace(">", " ")
    txt = txt.replace("\\", " ")
    txt = txt.replace("/", " ")
    txt = txt.replace("+", " ")
    #txt = txt.replace(";", " ")  # deactivated because we need it for the url encoded special character liek &quot;
    txt = txt.replace(",", " ")
    txt = txt.replace('"', " ")

    txt = txt.replace(spacer, " ")

    return txt



def process_db_entry(lan, source, title, link, enc):

    if not check_if_url_done(link):

        set_url_done(link)
        resp = ""

        try:
            print("processing: " + link)
            resp = req.urlopen(link).read()
            txt = str(resp, encoding=enc)
            txt = html_2_text(txt)
            print(source + ": text : " + txt)
            handle_one_text(lan, txt)

        except:
            print("error")



def process_link(language, source, encoding, url, target_encoding):

    print("----------------------------------------------------------")
    print(language)
    print(source)
    print(encoding)
    print(url)
    print(target_encoding)

    # open the URL and read the response

    if len(url) < 10:
        return


    resp = req.urlopen(url).read()

    # s = str(resp, encoding='utf-8')
    # s = str(resp, encoding='ISO-8859-1')
    s = str(resp, encoding=encoding)

    root = ET.fromstring(s)

    for item in root.iter('item'):

        entry = {}
        entry["language"] = language
        entry["source"] = source
        entry["encoding"] = encoding
        entry["target_encoding"] = target_encoding

        # print("#######################################################")

        for title in item.iter('title'):
            # print(html_2_text(title.text))
            entry["title"] = html_2_text(title.text)

        #print("-------------------------------------------------------")

        for title in item.iter('description'):
            # print(html_2_text(title.text))
            entry["description"] = html_2_text(title.text)

        #print("-------------------------------------------------------")

        for title in item.iter('encoded'):
            # print(html_2_text(title.text))
            entry["encoded"] = html_2_text(title.text)

        #print("-------------------------------------------------------")

        for title in item.iter('link'):
            # print("LINK: " + title.text)
            entry["link"] = str(title.text).strip()

        db.append(entry)


# ======================================================================================================================
# START of program

with open("./config.json") as json_file:
    #j = json.load(json_file)
    s = json_file.read()

j = json.loads(s)

for language in j["LANGUAGES"]:

    link_list = j[language]

    for link in link_list:
        process_link(language, link["title"], link["encoding"], link["url"], link["target_encoding"])



# EXPORT

# print(db)
random.shuffle(db)

# create html code


html = ""
html += "<!DOCTYPE html>"
html += "<html>"
html += "<head>"
html += '<meta charset="UTF-8">'
html += "</head>"
html += "<body style='font-family:Arial, Helvetica, sans-serif;'>"

html += strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "<br>"


html += "<table border=1>"

for entry in db:

    html += "<tr>"

    html += "<td style='padding: 5px;'>"
    html += wrap_link(entry["language"], entry["link"])
    html += "</td>"

    html += "<td style='padding: 5px;'>"
    html += wrap_link(entry["title"], entry["link"])
    html += "</td>"

    html += "<td style='padding: 5px;'>"
    html += wrap_link(entry["source"], entry["link"])
    html += "</td>"

    #html += "<td>"
    #html += wrap_link(entry["description"], entry["link"])
    #html += "</td>"

    #html += "<td>"
    #html += wrap_link(entry["encoded"], entry["link"])
    #html += "</td>"

    if len(entry["target_encoding"]) < 3:
        enc = str(entry["encoding"]).strip()
    else:
        enc = str(entry["target_encoding"]).strip()


    process_db_entry(entry["language"], entry["source"], entry["title"], entry["link"], enc)

    html += "</tr>"

    html += "\n"


html += "</table>"

html += "</body>"

html += "</html>"

print(html)

file = open("../html/rss.html", "w",  encoding='utf-8')

file.write(html)

file.close()