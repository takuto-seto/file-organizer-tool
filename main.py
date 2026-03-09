from datetime import datetime
from pathlib import Path
import json
import sys
import os



def load_rules(config_path):
    if not config_path.exists():
        print(f"[error] {config_path}が見つかりません。")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            rules = json.load(f)

            if not rules:
                print("設定ファイルの中身が空です。")
                sys.exit(1)
            
        return rules
          
    except json.JSONDecodeError as e:    
        print(f"[error] {config_path}設定ファイルの形式が正しくありません。")
        sys.exit(1)

def main():

    base_path = Path(__file__).parent

    config_file = base_path / "config.json"
    rules = load_rules(config_file)


    target_dir_str = rules.get("target_directory", "~")
    target_path = Path(target_dir_str).expanduser()

    if not target_path.exists() or not target_path.is_dir():
        print(f"[error] ターゲットディレクトリが見つかりません。: {target_dir_str}")
        sys.exit(1)

    is_dry_run = rules.get("dry_run", False)
    if is_dry_run:
        print("シュミレーションモードです。実際にファイル操作はされません。")


    sort_map = {}
    report = {}

    try:
        for folder_name, extensions in rules.get("rules", {}).items():
            for ext in extensions:
                sort_map[ext] = folder_name

    except AttributeError as e:
        print("移動できるファイルがありません。")


    log_folder = base_path / "Logs"
    log_folder.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y%m%d")
    log_path = log_folder / f"{today}_sort.log"
    exclude_keywords = rules.get("exclude_keywords", [])

    with open(log_path, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        log_start = f">>>>>>>>>>>移動を開始します\n"
        if is_dry_run:
            f.write(f"{now}:[シミュレーション]{log_start}")
        
        else:
            f.write(f"{log_start}")

        for item in list(target_path.iterdir()):

            if item.is_dir():
                continue

            if item.is_file():

                skip_file = False
                for keyword in exclude_keywords:
                    if keyword.lower() in item.name.lower():
                        skip_file = True
                        break

                if skip_file:
                    print(f"除外ファイル:{item.name}")
                    continue
                    

                ext = item.suffix
                if ext in sort_map:
                    folder_name = sort_map[ext]                 
                    dest_dir = target_path / folder_name
                    
                    if is_dry_run:
                            print(f"[シミュレーション]移動予定: {item.name} {target_path} -> {folder_name}")

                    else:
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

                    report[folder_name] = report.get(folder_name, 0) + 1


        table_title = "リザルト(シミュレーション)" if is_dry_run else "リザルト"
        summary_header = f"\n{"="*15}{table_title:^21}{"="*15}\n"
        table_header = f"{"<引越し先のフォルダ名>":>35} |{"<処理回数>":>10} |"
        separator = f"{"-" * 46}+{"-" * 16}"

    print(summary_header)
    print(table_header)
    print(separator)

    total_count = 0

    for folder, count in report.items():
        log_msg = f"{folder:>45} |{count:>14} |\n{"-"*63}"
        print(f"{log_msg}")
        total_count += count
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
    table_footer = f"{"合計":>43} |{total_count:>14} |"
    log_comp = f"{table_footer}"

    print(f"{log_comp}")
    print(separator)
    print(f"\n{">"*10}移動処理終了")

    if __name__ = "__main__":
        main()
