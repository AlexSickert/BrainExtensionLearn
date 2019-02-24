
import json


# ToDo: If this does not load then the entore applicaiton should not load. Put it in a try catch and then shut down
# the app if not loading

parameters = json.load(open('./config.json'))

slaves_arr = parameters["slaves"]

slaves = {}

for s in slaves_arr:
    slaves[s[0]] = [s[1], s[2]]


slave_id = "" # the real value is being set by command line argument.