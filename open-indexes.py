from pathlib import Path
import os

base = Path.cwd() / "content"

indexed = {}

for index in base.rglob("Index.md"):
    for line in index.read_text().splitlines():
        if "weight:" in line:
            weight = line.split()[1].strip()
            rel_path = index.relative_to(base)
            indexed[weight] = index

for wt in sorted(indexed.keys()):
    print("{}: {}".format(wt, indexed[wt].relative_to(base)))
    os.system("subl {}".format(indexed[wt]))
