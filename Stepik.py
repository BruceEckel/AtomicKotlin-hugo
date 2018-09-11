import requests
from collections import OrderedDict
import os
from pathlib import Path
import json
from pprint import pprint
# To use a password:
# requests.get('raw.github.com/myfile.txt';, auth=('username', 'passwd'))
# ghusername = os.environ['GHUSER']
# ghpwd = os.environ['GHPWD']
# r = requests.get(url, auth=(ghusername, ghpwd))

url = 'https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrGz28CehT1_sax-80UaRSF5836BWks5bn_1XwA%3D%3D'
r = requests.get(url)

stepikLessonIDs = OrderedDict()

for line in r.text.splitlines():
    line = line.strip()
    if line:
        k, v = line.split("=")
        stepikLessonIDs[k] = v

# for k, v in stepikLessonIDs.items():
#     print(f"{k} -> {v}")

# jsonarray = json.dumps(stepikLessonIDs)
# pprint(jsonarray)

githome = Path(os.environ['GIT_HOME'])
atomickotlin = githome / "AtomicKotlin" / "MarkDown"
hugo = githome / "AtomicKotlin-hugo" / "data"

markdown = sorted([(md.name, md.name[4:-3]) for md in atomickotlin.glob("*.md")])

def test(name):
    for sname, sid  in stepikLessonIDs.items():
        if sname == name:
            return sname, sid
        if name.startswith("Section_") and name.endswith(sname):
            return sname, sid
    return False, False

with Path('InStepik.html').open(mode='w') as f:
    for name in markdown:
        inStepik, sid = test(name[1])
        if inStepik:
            print(f"{name[0]} : {inStepik} -> {sid}<br>", file=f)
        else:
            print(f'<span style="background-color: red">{name[0]} not in Stepik</span><br>', file=f)
