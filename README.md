# file-organizer-tool
- 指定されたディレクトリ内のファイルを、拡張子に基づいて自動的にフォルダ分けするPythonツールです。


# Demo

## console出力
実行時の進捗と最終的な集計結果が一目で確認できます。

```bash
読み込まれたルール:{'Documents': ['.txt', '.pdf'], 'Data': ['.csv', '.xlsx']}
変換後のルール{'.txt': 'Documents', '.pdf': 'Documents', ...}

移動完了: /Users/seto/Project/Documents -> Documents
[error] report_v1.xlsx の移動ができませんでした。：[Errno 13] Permission denied
移動完了: /Users/seto/Project/Data -> Data

フォルダ名：Documents/カウント回数：5回
フォルダ名：Data/カウント回数：3回
```

## 生成されるログファイル (sort.log)
例外が発生した際の理由や、秒単位の処理記録が永続的に保存されます。

```bash
2026-03-02 21:00:00 :>>>>>>>>>>>移動を開始します
2026-03-02 21:00:01 :[移動成功] manual.pdf -> Documents
2026-03-02 21:00:02 :[error] report_v1.xlsx の移動ができませんでした。：[Errno 13] Permission denied: 'report_v1.xlsx'
2026-03-02 21:00:03 :[移動完了] フォルダ名：Documents に 5回 移動しました
2026-03-02 21:00:03 :[移動完了] フォルダ名：Data に 3回 移動しました
2026-03-02 21:00:03 :>>>>>>>>>>>[処理完了]
```



# Features
- 自動フォルダ振り分け: 拡張子ごとにあらかじめ定義されたフォルダへ自動移動します。
- 高度な重複回避（リネーム機能）: 移動先に同名ファイルが存在する場合、(1), (2) のように空き番号が見つかるまで自動で連番を付与し、既存ファイルの上書きを防止します。

- 実行結果の集計表示: 処理完了後、各カテゴリ（フォルダ）ごとに何件のファイルを移動したかのサマリーを表示します。

- 外部設定ファイル（JSON）対応: 振り分けルールを config.json で管理しているため、プログラムを修正せずに拡張子の追加や変更が可能です。

- 例外処理機能: 処理中にファイルがロックされている、あるいはアクセス権限がない場合でも、エラー内容を記録して次のファイル処理を継続します。

- 詳細なロギング: 実行時刻、移動の成否、最終的な集計結果を sort.log ファイルへ自動記録します。

# Requirement
- Python 
- 使用ライブラリ: pathlib, json, 

# App Profile
- 開発ツール: VSCode / Wakatime（作業時間の可視化）
- 管理手法: Studyplusによる学習記録、GitHubでのブランチ運用・PR管理

# Installation
- リポジトリをクローンし、対象のディレクトリへ移動します。

```bash
git clone [https://github.com/t-seto/file-organizer-tool.git](https://github.com/t-seto/file-organizer-tool.git)
cd file-organizer-tool
```

# Usage
- config.json を編集し、仕分けたいフォルダ名と拡張子のペアを記述します。
- 整理したいファイル群と同じ階層に main.py を配置し、実行します。

```bash
python main.py
```

# Note
- 安全な反復処理: pathlib.iterdir() をリストとしてスナップショット化してからループを回すことで、処理中のファイル移動に伴う FileNotFoundError を回避する設計にしています。

- パス操作の堅牢性: OS依存の文字列結合を避け、pathlib の / 演算子や with_stem() を活用してパスを生成しています。

- ログ管理: ログは追記モードで保存されるため、過去の履歴もすべて保持されます。

- エンコーディング: 日本語のファイル名やフォルダ名に対応するため、UTF-8エンコーディングでログを書き込みます

# Author
t.seto
