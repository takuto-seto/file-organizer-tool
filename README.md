# file-organizer-tool
- 指定されたディレクトリ内のファイルを、拡張子に基づいて自動的にフォルダ分けするPythonツールです。

# Demo

```bash
読み込まれたルール:{'Documents': ['.txt', '.pdf'], 'Data': ['.csv', '.xlsx']}
移動完了: /Users/.../Documents -> Documents
...
フォルダ名：Documents/カウント回数：3回
フォルダ名：Data/カウント回数：1回
```

# Features
- 自動フォルダ振り分け: 拡張子ごとにあらかじめ定義されたフォルダへ自動移動します。
- 高度な重複回避（リネーム機能）: 移動先に同名ファイルが存在する場合、(1), (2) のように空き番号が見つかるまで自動で連番を付与し、既存ファイルの上書きを防止します。

- 実行結果の集計表示: 処理完了後、各カテゴリ（フォルダ）ごとに何件のファイルを移動したかのサマリーを表示します。

- 外部設定ファイル（JSON）対応: 振り分けルールを config.json で管理しているため、プログラムを修正せずに拡張子の追加や変更が可能です。

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

# Author
t.seto
