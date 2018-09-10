import requests
from collections import OrderedDict
import os
import json
from pprint import pprint
# To use a password:
# requests.get('raw.github.com/myfile.txt';, auth=('username', 'passwd'))
url = 'https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrGz28CehT1_sax-80UaRSF5836BWks5bn_1XwA%3D%3D'
# ghusername = os.environ['GHUSER']
# ghpwd = os.environ['GHPWD']
# r = requests.get(url, auth=(ghusername, ghpwd))
r = requests.get(url)

stepikLessonIDs = OrderedDict()

for line in r.text.splitlines():
    line = line.strip()
    if line:
        k, v = line.split("=")
        stepikLessonIDs[k] = v

for k, v in stepikLessonIDs.items():
    print(f"{k}: {v}")

jsonarray = json.dumps(stepikLessonIDs)
pprint(jsonarray)
