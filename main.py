import json
from pathlib import Path
import shutil

def load_rules(config_path):
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
base_path = Path(__file__).parent

config_file = base_path / "config.json"
rules = load_rules(config_file)

print(f"読み込まれたルール:{rules}")


sort_map = {}
for folder_name, extensions in rules.items():
    for ext in extensions:
        sort_map[ext] = folder_name

print(f"変換後のルール{sort_map}")


for item in base_path.iterdir():

    if item.is_file() and item.name not in [Path(__file__).name, "config.json"]:
        ext = item.suffix
        if ext in sort_map:
            folder_name = sort_map[ext]
            dest_dir = base_path / folder_name
            base_path.mkdir(parents=True, exist_ok=True)

            item.rename(dest_dir)
            print(f"移動完了: {dest_dir} -> {folder_name}")