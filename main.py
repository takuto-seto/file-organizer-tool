import json
from datetime import datetime
from pathlib import Path

def load_rules(config_path):
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
base_path = Path(__file__).parent

config_file = base_path / "config.json"
rules = load_rules(config_file)

print(f"読み込まれたルール:{rules}")


sort_map = {}
report = {}

for folder_name, extensions in rules.items():
    for ext in extensions:
        sort_map[ext] = folder_name

print(f"変換後のルール{sort_map}")

log_path = base_path / "sort.log"
with open(log_path, "a", encoding="utf-8") as f:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    log_start = f"{now}:>>>>>>>>>>>移動を開始します\n"
    f.write(f"{log_start}")

    for item in list(base_path.iterdir()):

        if item.is_file() and item.name not in [Path(__file__).name, "config.json", "sort.log"]:
            ext = item.suffix
            if ext in sort_map:
                folder_name = sort_map[ext]
                
                dest_dir = base_path / folder_name
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                dest_path = dest_dir / item.name
                copy_count = 1 
                # 重複チェック
                while dest_path.exists():
                    dest_path = dest_dir / f"{item.stem}({copy_count}){item.suffix}"
                    copy_count += 1

                
                try:
                    # 移動処理の実行            
                    item.rename(dest_path)

                except Exception as e:
                    print(f"[error] {item.name} の移動ができませんでした。：{e}")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                    log_err = f"[error] {item.name} の移動ができませんでした。：{e}"
                    f.write(f"{now}:{log_err}\n")
                    continue

        
                print(f"移動完了: {dest_dir} -> {folder_name}")
                report[folder_name] = report.get(folder_name, 0)
                report[folder_name] += 1

    for folder, count in report.items():
        print(f"フォルダ名：{folder}/カウント回数：{count}回")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        log_msg = f"[移動完了] フォルダ名：{folder} に {count}回 移動しました"
        f.write(f"{now}:{log_msg}\n")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    log_comp = ">>>>>>>>>>>[処理完了]"
    f.write(f"{now}:{log_comp}\n\n")