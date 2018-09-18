import requests
from collections import OrderedDict
import os
from pathlib import Path
import json
import pprint
# To use a password:
# requests.get('raw.github.com/myfile.txt';, auth=('username', 'passwd'))
# ghusername = os.environ['GHUSER']
# ghpwd = os.environ['GHPWD']
# r = requests.get(url, auth=(ghusername, ghpwd))

url = 'https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrLAIxCt9tChPNfSEwPLdtCwrghTDks5bqXAgwA%3D%3D'
githome = Path(os.environ['GIT_HOME'])
atomickotlin = githome / "AtomicKotlin" / "MarkDown"
hugoData = githome / "AtomicKotlin-hugo" / "data"
# markdown = set([(md.name, md.name[4:-3]) for md in atomickotlin.glob("*.md")])
markdown = set([md.name[4:-3] for md in atomickotlin.glob("*.md")])

class StepikLessonID:
    def __init__(self, line):
        assert line.strip(), "Line cannot be empty"
        _name, self.id = line.split("=")
        if self.id == "0": # It's a section
            for md in markdown:
                if _name in md:
                    self.name = md.replace('_', ': ', 2).replace('Section: ', 'Section ').replace('_', ' ')
        elif _name in markdown:
            self.name = _name.replace('_', ' ')
        else:
            self.name = "Not found"
    def __repr__(self):
        return str(self.__dict__)

lesson_ids = [StepikLessonID(line) for line in requests.get(url).text.strip().splitlines() if line.strip()]

class StepikEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StepikLessonID):
            return obj.__dict__
        # Base class default() raises TypeError:
        return json.JSONEncoder.default(self, obj)

if not hugoData.exists():
    hugoData.mkdir()
(hugoData / "atomNames.json").write_text(json.dumps(lesson_ids, cls=StepikEncoder, indent=2))

# def test(name):
#     for sname, sid  in stepikLessonIDs.items():
#         if sname == name:
#             return sname, sid, sname
#         if name.startswith("Section_") and name.endswith(sname):
#             return name, sid, sname
#     return False, False, False

# with Path('InStepik.html').open(mode='w') as f:
#     for name in markdown:
#         inStepik, sid, _ = test(name[1])
#         if inStepik:
#             print(f"{name[0]} : {inStepik} -> {sid}<br>", file=f)
#         else:
#             print(f'<span style="background-color: red">{name[0]} not in Stepik</span><br>', file=f)

# mdNames = set([md[1] for md in markdown])

# lessonIDs = OrderedDict()

# for k, v in stepikLessonIDs.items():
#     if v == "0": # It's a section
#         for n in mdNames:
#             if k in n:
#                 n = n.replace('_', ': ', 2)
#                 n = n.replace('Section: ', 'Section ')
#                 n = n.replace('_', ' ')
#                 lessonIDs[n] = "0"
#     elif k in mdNames:
#         lessonIDs[k.replace('_', ' ')] = v


# class Stepik:
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id
#         self.foo = "bar"
#     def json(self):
#         return f'    {{ "name": "{self.name}",  "id": "{self.id}" }},\n'


# class StepikJSONList:
#     def __init__(self, item_list):
#         self.item_list = item_list
#         self.json_list = "[\n"
#         for item in item_list:
#           self.json_list += item.json()
#     def __str__(self):
#         result = self.json_list.rstrip().rstrip(',')
#         return result + "\n]"
#     def json(self):
#         for item in self.item_list:
#             print(json.dumps(item.__dict__))

# LessonIDList = StepikJSONList([Stepik(nm, id) for nm, id in lessonIDs.items()])
# # print(LessonIDList)

# if not hugoData.exists():
#     hugoData.mkdir()
# atoms = hugoData / "atomNames.json"
# atoms.write_text(str(LessonIDList))

# LessonIDList.json()
