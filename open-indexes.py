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
    print(f"{wt}: {indexed[wt].relative_to(base)}")
    os.system(f"subl {indexed[wt]}")

config_toml = Path.cwd() / "config.toml"
if config_toml.exists():
    os.system(f"subl {config_toml}")

