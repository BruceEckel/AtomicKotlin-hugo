import requests
from collections import OrderedDict
import os
import sys
from pathlib import Path
import json
import pprint

# To use a password:
# requests.get('raw.github.com/myfile.txt';, auth=('username', 'passwd'))
# ghusername = os.environ['GHUSER']
# ghpwd = os.environ['GHPWD']
# r = requests.get(url, auth=(ghusername, ghpwd))

url = "https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrJlStD3fNxWb2DZfvOKXXNxaMieSks5bqo6awA%3D%3D"
githome = Path(os.environ["GIT_HOME"])
atomickotlin = githome / "AtomicKotlin" / "MarkDown"
hugoData = githome / "AtomicKotlin-hugo" / "data"
# markdown_names = set(md.name[4:-3] for md in atomickotlin.glob("*.md"))
markdown_names = set(md.name for md in atomickotlin.glob("*.md"))


class StepikLessonID:
    @staticmethod
    def match_lesson_name(lesson_name, id):
        for md_name in markdown_names:
            if lesson_name == md_name[4:-3]:
                return md_name #, md_name[4:-3].replace("_", " ")
        if id == "0":  # It's a section
            for md_name in markdown_names:
                if lesson_name in md_name:
                    return md_name
                    # return (
                    #     md_name,
                    #     md_name[4:-3]
                    #     .replace("_", ": ", 2)
                    #     .replace("Section: ", "Section ")
                    #     .replace("_", " "),
                    # )
        return "Not found" #, "Not found"

    def __init__(self, lesson_line):
        assert lesson_line.strip(), "Line cannot be empty"
        self.lesson_name, self.id = lesson_line.split("=")
        self.md_name = StepikLessonID.match_lesson_name(self.lesson_name, self.id)
        if self.md_name.endswith(".md"):
            self.title = (atomickotlin / self.md_name).read_text().splitlines()[0].strip()
        else:
            self.title = "Not Found"

    def __repr__(self):
        return str(self.__dict__)


request = requests.get(url)
if str(request.status_code).startswith("4"):
    print(f"Status code: {request.status_code}")
    sys.exit()

lesson_ids = [
    StepikLessonID(line) for line in request.text.strip().splitlines() if line.strip()
]

class StepikEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StepikLessonID):
            return obj.__dict__
        # Base class default() raises TypeError:
        return json.JSONEncoder.default(self, obj)


if not hugoData.exists():
    hugoData.mkdir()
(hugoData / "atomNames.json").write_text(
    json.dumps(lesson_ids, cls=StepikEncoder, indent=2)
)
