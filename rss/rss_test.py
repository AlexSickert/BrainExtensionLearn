
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

def get_dictionary(name):

    #print("get dictionary: " + name)

    file_name = name + ".pickle"

    if os.path.isfile(file_name):
        fileObject = open(file_name, 'rb')
        # load the object from the file into var b
        ret = pickle.load(fileObject)

    return ret


x = get_dictionary("RUSSIAN")

for y in x:
    print(y, x[y])
