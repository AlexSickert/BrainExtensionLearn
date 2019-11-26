
from os import walk
import rss_parser as rss_parser



f = []
for (dirpath, dirnames, filenames) in walk("./texts"):
    f.extend(filenames)


for f in filenames:
    if "RAW" in f:
        #print(f)

        fi = open("./texts/" + f, "r")
        txt = fi.read()
        fi.close()

        txt_read = rss_parser.parse(txt, f, f)
