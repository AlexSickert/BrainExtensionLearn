#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 12:01:09 2017

@author: alex
"""
  
import urllib.request
import re
import operator

resource = urllib.request.urlopen('http://www.lemonde.fr/ameriques/article/2016/09/01/premier-vol-regulier-usa-cuba-en-55-ans_4990719_3222.html') 

#resource = urllib.request.urlopen('http://forbes.ru/') 

#http://www.forbes.ru/

html =  resource.read().decode(resource.headers.get_content_charset())

txt = str(html) + " " 
                       
txt = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", txt)  
txt = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", txt)                         
txt = re.sub(r"<.+?>", " ", txt)

txt = re.sub(r",", " ", txt)
#txt = re.sub(r""", " ", txt)
txt = re.sub(r"»", " ", txt)
txt = re.sub(r"«", " ", txt)
txt = re.sub(r"\.", " ", txt)
txt = re.sub(r":", " ", txt)
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
txt = re.sub(r"&#9642;", "", txt) #black small square

arr = txt.split(" ")

dic = {}

for w in arr:
    if len(w) > 1:
        
        wc = w.strip()
        
        if wc in dic:
#            print("existis: " + w )
            dic[wc] = dic[wc] + 1
        else:
            dic[wc] = 1
        
        
#import operator
#x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(dic.items(), key=operator.itemgetter(1))        
#print(sorted_x[len(sorted_x) - 1 ])
print(sorted_x)

#import json
#
#
#from urllib.request import urlopen
##resp = urlopen('https://github.com')
#resp = urlopen('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=de&dt=t&q=miscarriages')
#
#print(resp.read())
#
#url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=de&dt=t&q=miscarriages'
#
#import urllib.request, ssl
#
#
#https_sslv3_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv3))
#opener = urllib.request.build_opener(https_sslv3_handler)
#urllib.request.install_opener(opener)
#resp = opener.open(url)
#html = resp.read().decode('utf-8')
#print(html)



#
#resp = urlopen('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=de&dt=t&q=miscarriages') 
#
##http://www.forbes.ru/
#
#j =  resp.read()
#
#j = str(j) + " "
#
##j = '[[["Fehlgeburten","miscarriages",null,null,3]],null,"en"]'
#xxx = json.loads(j)
#
#print(xxx)
#
#translatedText = xxx[0][0][0]
#                    
#print(translatedText)
#
##transpation https://cloud.google.com/translate/docs/reference/translate#body.QUERY_PARAMETERS 
## https://cloud.google.com/translate/docs/translating-text
## https://cloud.google.com/translate/docs/reference/libraries
#
#
#



