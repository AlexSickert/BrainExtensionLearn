
import xml.etree.ElementTree as ET
import urllib.request  as req
import re
import random
import json
import os.path
import pickle
from time import gmtime, strftime
import time
import os
import random

#import rss.rss_parser as rss_parser
import rss_parser as rss_parser

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

        v = dic[url]

        if v:
            if len(str(v)) > 10:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def get_local_file(url):

    dic = get_dictionary("URLs")
    v = ""

    if url in dic:
        v = dic[url]

    return v

def set_url_done(url, localFile):

    dic = get_dictionary("URLs")
    dic[url] = localFile
    save_dictionary("URLs", dic)


def wrap_link(txt, lnk, is_local):

    ret = "<a href='"
    ret += lnk
    ret += "' ratget='_blank'>"
    ret += txt
    if is_local:
        ret += ""
    ret += "</a>"
    return ret



def get_file_nem(lang, url, source):

    h = hash(url)

    if h < 1:
        h = -1 * h

    ret = lang + "_" + str(source) + "_" + str(h) + ".txt"
    ret = ret.replace(" ", "_")

    return ret


def make_local_link(lang, url, source):


    fn = "./texts/" + get_file_nem(lang, url, source)

    if os.path.exists(fn):
        print("local link exists: " + str(fn))
        return get_file_nem(lang, url, source)
    else:
        print("local link does NOT exist: " + str(fn))
        return None






def save_raw_text_as_file(lang, txt, url, source, flag):

    #create folder if not exists

    dirname = "./texts/"

    if not os.path.exists(os.path.dirname(dirname)):
        try:
            os.makedirs(os.path.dirname(dirname))
        except:
            print("error making directory")


    h = hash(url)

    if h < 1:
        h = -1 * h


    fn = dirname + lang + "_" + str(source) + "_" + str(h) + "-" + flag + ".txt"
    fn = fn.replace(" ", "_")
    f = open(fn, "w+", encoding="utf-8")
    f.write(txt)
    f.close()



def save_text_as_file(lang, txt, url, source):

    #create folder if not exists

    dirname = "./texts/"

    if not os.path.exists(os.path.dirname(dirname)):
        try:
            os.makedirs(os.path.dirname(dirname))
        except:
            print("error making directory")


    h = hash(url)

    if h < 1:
        h = -1 * h

    fn = dirname + get_file_nem(lang, url, source)
    #fn = fn.replace(" ", "_")
    f = open(fn, "w+", encoding="utf-8")
    f.write(txt)
    f.close()

    fn = dirname + lang + "_" + str(source) + "_" + str(h) + ".html"
    fn = fn.replace(" ", "_")
    f = open(fn, "w+", encoding="utf-8")
    f.write(txt)
    f.close()

    #print("alksdjf ;alkjsdf ;alkjsdf ;laj**************+++++++++")

    return get_file_nem(lang, url, source)


def get_top_naiv(link):

    navi = """
    
        <table style="width: 100%">
            <tr>
                <td>#home#</td>
                <td><a onclick="smaller();">&nbsp;-&nbsp;</a></td>
                <td><a onclick="bigger();">&nbsp;+&nbsp;</a></td>
                <td>#orig#</td>
            </tr>        
        <table>  <br><br>
    
    """
    orig = "<a href='" + link + "'>ORIGINAL</a>"
    home = " <a href=\"./rss.html\">HOME</a><br>"

    navi = navi.replace("#home#", home)
    navi = navi.replace("#orig#", orig)

    return navi


def add_js(link, lan, txt_read, title):

    ret = ""

    arr = title.split(" ")
    ti = ""
    if len(arr) > 0:

        for ele in arr:
            if len(ele) > 0:
                e = ele.strip()
                ti += "<span  onclick=\"translateMe(this, \'" + e + "\', \'" + lan + "\')\">" + e + " </span> \n"
        ret += "<h1>" + ti + "</h1><br><br>"
    else:
        ret += "<h1>" + title + "</h1><br><br>"

    arr = txt_read.split(" ")

    js = """
    
    <link rel = "stylesheet" type = "text/css" href = "./rss.css" />
    
    <style>
    
    </style>
    
    <script src="./rss.js"></script>
    
    <script>
    
    
    
    
    function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
    
    var globalFontSize = 20;
    
    function smaller(){
    
        updateFontSize(-2);
    }
    
    function bigger(){
        
        updateFontSize(2);
    }
    
    
    
    function updateFontSize(delta) {
    
        console.log("updateFontSize  = " + delta);

        globalFontSize = parseInt(globalFontSize) + parseInt(delta);        
        setCookie("RssGlobalFontSize", globalFontSize, 1000);               
        setSize(globalFontSize);
    };
    
    
    function setSize(s){
    
        console.log("setting size to  = " + s);
    
        var all = document.getElementsByTagName("*");
        
        for (var i = 0, max = all.length; i < max; i++) {
            try {
                all[i].style.fontSize = parseInt(s).toString() + "px";
            } catch (e) {
                // to do;
                console.log("error in setSize  = " + e);
            }
        }  
        
        all = document.getElementsByTagName("a");
        
        for (var i = 0, max = all.length; i < max; i++) {
            try {
                var n = parseInt(s) * 1.5;
                all[i].style.fontSize = n.toString() + "px";
            } catch (e) {
                // to do;
            }
        }
        
        console.log("finished setting size to  = " + s);
        
        
    }
    
    function loadFontSize(){
    
        var x = getCookie("RssGlobalFontSize");
        
        console.log("RssGlobalFontSize = " + x);
        
        if (x.length > 0){
            globalFontSize = x;
            setSize(x);
        }else{
            globalFontSize = 30;
            setSize(30);
        }      
    }
    
    </script>
    """

    if len(arr) > 0:

        for ele in arr:
            if len(ele) > 0:
                e = ele.strip()
                e = e.replace("\n", " ")
                e = e.replace("\r", " ")
                e = e.replace("\t", " ")
                e = e.replace("\'", "&apos;")
                e = e.replace("\"", "&quot;")

                ret += "<span onclick=\"translateMe(this, '" + e + "', '" + lan + "')\">" + e + " </span> "
        return js + ret
    else:
        return txt_read


def process_db_entry(lan, source, title, link, enc, always_load = False):

    print("--------------------------------")
    print("processing " + link)

    if (not check_if_url_done(link)) or always_load:


        resp = ""

        print("url not done yet: " + str(link))

        try:
            print("processing: " + link)
            resp = req.urlopen(link).read()
            txt = str(resp, encoding=enc)
            #txt = rss_parser.html_2_text(txt)
            print(source + ": text : " + txt)


            handle_one_text(lan, txt)

            txt_read = str(resp, encoding=enc)

            save_raw_text_as_file(lan, txt_read, link, source, "RAW")


            txt_read = rss_parser.parse(txt_read, lan, source)


            save_raw_text_as_file(lan, txt_read, link, source, "CLEAN")

            txt_read = add_js(link, lan, txt_read, title)

            txt_read = get_top_naiv(link)  + txt_read

            txt_read = "<body onload=\"loadFontSize();\">" + txt_read + "<div onclick=\"hideTranslate()\" id=\"translate\">loading...</div></body>"

            ret = save_text_as_file(lan, txt_read, link, source)



            print("new processed file is: " + str(ret))

            set_url_done(link, ret)

            return ret
        except Exception as ex:
            print("error: " + str(ex))
            return None

    else:

        return get_local_file(link)


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

    try:

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
                entry["title"] = rss_parser.html_2_text(title.text)

            #print("-------------------------------------------------------")

            for title in item.iter('description'):
                # print(html_2_text(title.text))
                entry["description"] = rss_parser.html_2_text(title.text)

            #print("-------------------------------------------------------")

            for title in item.iter('encoded'):
                # print(html_2_text(title.text))
                entry["encoded"] = rss_parser.html_2_text(title.text)

            #print("-------------------------------------------------------")

            for title in item.iter('link'):
                # print("LINK: " + title.text)
                entry["link"] = str(title.text).strip()

            db.append(entry)

    except Exception as ex:

        print("error: ", ex)



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


# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================


random.shuffle(db)

# create html code


html = ""
html += "<!DOCTYPE html>"
html += "<html>"
html += "<head>"
html += '<meta charset="UTF-8">'
html += '<meta name="viewport" content="width=device-width, initial-scale=1">'



st = """
    
    <link rel = "stylesheet" type = "text/css" href = "./rss.css" />
    
    <script>
    
    function shuffle(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;
    
      // While there remain elements to shuffle...
      while (0 !== currentIndex) {
    
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
    
        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }
    
      return array;
    }
    
    function reorder(){
    
        i_max = document.getElementById("i_count").innerHTML;
console.log("i_max = " + i_max);
i_max =  parseInt(i_max , 10);
        console.log("i_max = " + i_max);
        
        var arr = [];
        
        for (i = 0; i < i_max; i++) {
            arr.push(i+1);
        }
        
        arr = shuffle(arr);
        
        html = "";
        
        for (i = 0; i < i_max; i++) {
        
            try{
            x = arr[i];
            
            h = document.getElementById("row_source_" + x).innerHTML;
            
            html += '<tr id="row_source_' + x + '">' + h + "</tr>";
            
            h = document.getElementById("row_title_" + x).innerHTML;
            
            html += '<tr id="row_title_' + x + '">' + h + "</tr>";
            }catch(e){
            console.log("---------------");
            console.log(e);
            console.log("---------------");
            }
            
        } // end for
       
        var table = document.getElementById("content-table");
            
        table.innerHTML = html;
       
    } // end function
        
</script>


"""

html += st


html += "</head>"
html += "\n<body onload=\"reorder()\">"

html += strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "&nbsp;V-19-08-17-A "
html += "<span onclick=\"reorder()\">SHUFFLE</span>"
html += "\n<table id=\"content-table\" border=0>"

db_entry_td_arr = []  # array that holds the entries which gets shuffeled
i = 0
for entry in db:

    if len(entry["target_encoding"]) < 3:
        enc = str(entry["encoding"]).strip()
    else:
        enc = str(entry["target_encoding"]).strip()

    rss_link_local = process_db_entry(entry["language"], entry["source"], entry["title"], entry["link"], enc)

    #
    if rss_link_local is not None:
        if len(rss_link_local) > 0:
            i += 1
            x = wrap_link(entry["title"], "./rss_content_" + rss_link_local, True)

            trs = ""

            trs += "\n<tr id=\"row_source_" + str(i) + "\" >"

            trs += "<td class='language'>"
            trs += entry["language"]
            trs += "</td> "

            trs += " <td class='source'>"
            trs += entry["source"]
            trs += "</td> "

            trs += "</tr>"

            trs += "\n<tr id=\"row_title_" + str(i) + "\" >"

            trs += "<td colspan=\"2\" style='border-bottom: 3px solid #cccccc; padding-bottom: 10px;'>"

            trs += x

            #else:
                #trs += wrap_link(entry["title"], entry["link"], False)

            trs += "</td>"

            trs += "</tr>"

            trs += "\n"

            db_entry_td_arr.append(trs)

random.shuffle(db_entry_td_arr)

for ele in db_entry_td_arr:
    html += ele


html += "</table>"
html += "<div id=\"i_count\">" + str(i)+ "</div>"
html += "</body>"

html += "</html>"

print(html)

file = open("../html/rss.html", "w",  encoding='utf-8')

file.write(html)

file.close()

print("file was saved to ../html/rss.html")
