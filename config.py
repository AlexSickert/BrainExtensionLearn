
import json


# ToDo: If this does not load then the entore applicaiton should not load. Put it in a try catch and then shut down
# the app if not loading

parameters = json.load(open('./config.json'))

