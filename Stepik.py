import json
import os
import sys
from pathlib import Path
import requests

# To use a password:
# ghusername = os.environ['GHUSER']
# ghpwd = os.environ['GHPWD']
# r = requests.get(url, auth=(ghusername, ghpwd))
githome = Path(os.environ["GIT_HOME"])
markdown = githome / "AtomicKotlin" / "MarkDown"
hugo_data = githome / "AtomicKotlin-hugo" / "data"
hugo_json = hugo_data / "atomNames.json"

url = "https://raw.githubusercontent.com/JetBrains/AtomicKotlin/master/resources/stepikLessonIDs.properties?token=AA9JrGf-04wiPICt4A2oIX3HbhPK_TH1ks5br6S9wA%3D%3D"
request = requests.get(url)
if str(request.status_code).startswith("4"):
    print(f"Status code: {request.status_code}")
    sys.exit()


class Stepik:
    markdown_names = set(md.name for md in markdown.glob("*.md"))
    __items = None

    @staticmethod
    def match_lesson_name(lesson_name, id):
        for md_name in Stepik.markdown_names:
            if lesson_name == md_name[4:-3]:
                return True, md_name
        if id == "0":  # It's a section
            for md_name in Stepik.markdown_names:
                if lesson_name in md_name:
                    return True, md_name
            return False, lesson_name
        return False, lesson_name.replace("_", " ")

    def __init__(self, lesson_line):
        assert lesson_line.strip(), "Line cannot be empty"
        self.lesson_name, self.id = lesson_line.split("=")
        self.match, self.md_name = Stepik.match_lesson_name(self.lesson_name, self.id)
        if self.match:
            self.title = (markdown / self.md_name).read_text().splitlines()[0].strip()
        else:
            self.title = self.md_name

    @staticmethod
    def items():
        if not Stepik.__items:
            Stepik.__items = [
                Stepik(line)
                for line in request.text.strip().splitlines()
                if line.strip()
            ]
            Stepik.__items.append(Stepik("Section V: Object-Oriented Programming=0"))
            Stepik.__items.append(Stepik("Section VI: Power Tools=0"))
            Stepik.__items.append(Stepik("Section VII: Language Interoperability=0"))
        return Stepik.__items

    @staticmethod
    def show_missing_lessons():
        def find(md):
            for stp in Stepik.items():
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

    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Stepik):
                return obj.__dict__
            # Base class default() raises TypeError:
            return json.JSONEncoder.default(self, obj)


if not hugo_data.exists():
    hugo_data.mkdir()
hugo_json.write_text(json.dumps(Stepik.items(), cls=Stepik.Encoder, indent=2))

Stepik.show_missing_lessons()
