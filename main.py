import json
from pathlib import Path

def load_rules(config_path):
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
base_path = Path(__file__).parent

config_file = base_path / "config.json"
rules = load_rules(config_file)

print(f"読み込まれたルール:{rules}")