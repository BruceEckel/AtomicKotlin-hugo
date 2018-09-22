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

url = "https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrGf-04wiPICt4A2oIX3HbhPK_TH1ks5br6S9wA%3D%3D"
githome = Path(os.environ["GIT_HOME"])
atomickotlin = githome / "AtomicKotlin" / "MarkDown"
hugoData = githome / "AtomicKotlin-hugo" / "data"


class Stepik:
    markdown_names = set(md.name for md in atomickotlin.glob("*.md"))

    @staticmethod
    def match_lesson_name(lesson_name, id):
        for md_name in Stepik.markdown_names:
            if lesson_name == md_name[4:-3]:
                return md_name
        if id == "0":  # It's a section
            for md_name in Stepik.markdown_names:
                if lesson_name in md_name:
                    return md_name
        return None

    def __init__(self, lesson_line):
        assert lesson_line.strip(), "Line cannot be empty"
        self.lesson_name, self.id = lesson_line.split("=")
        self.md_name = Stepik.match_lesson_name(self.lesson_name, self.id)
        if self.md_name:
            self.title = (
                (atomickotlin / self.md_name).read_text().splitlines()[0].strip()
            )
        else:
            self.title = "Not Found"

    @staticmethod
    def show_missing_lessons(stepik_list):
        def find(md):
            for stp in stepik_list:
                if stp.md_name == md:
                    return stp
            return None

        with Path("InStepik.html").open(mode="w") as f:
            for md in sorted(Stepik.markdown_names):
                found = find(md)
                if found:
                    print(f"{found.title} : {found.id}<br>", file=f)
                else:
                    print(
                        f'<span style="background-color: red">{md}</span><br>', file=f
                    )


class StepikEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stepik):
            return obj.__dict__
        # Base class default() raises TypeError:
        return json.JSONEncoder.default(self, obj)


request = requests.get(url)
if str(request.status_code).startswith("4"):
    print(f"Status code: {request.status_code}")
    sys.exit()


stepik_list = [
    Stepik(line) for line in request.text.strip().splitlines() if line.strip()
]


if not hugoData.exists():
    hugoData.mkdir()
(hugoData / "atomNames.json").write_text(
    json.dumps(stepik_list, cls=StepikEncoder, indent=2)
)


Stepik.show_missing_lessons(stepik_list)
