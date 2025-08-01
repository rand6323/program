# ファイル整理アプリ

複数のファイルを拡張子、更新日時、カテゴリ別に整理する Python + Tkinter ベースのデスクトップアプリケーションです。

## 主な機能
このアプリは、指定したフォルダ内のファイルを以下の基準で自動的に整理します：

- 拡張子によるカテゴリ分け（例：画像、文書、音楽、動画）

- ファイルの更新日時に基づく年・月別のサブフォルダ作成

- 重複ファイル名の自動リネーム（例：file_1.jpg）

- 進捗バーと現在処理中のファイル名を表示するユーザーインターフェース

## 使用技術
Python 3.13

Tkinter（標準ライブラリ）

shutil、os、logging、datetime（標準ライブラリ）

## ディレクトリ構成

```
file-organizer/
├── organizer.py       # メインアプリケーション
├── requirements.txt   # 必要なライブラリ
├── README.md          # このファイル
├── LICENSE.txt        # MITライセンス
└── .gitignore         # Git 管理から除外するファイル
```

## セットアップ
```
git clone https://github.com/rand6323/file-organizer.git
cd file-organizer
```

## スクリーンショット

画面

![画面](./images/file_organizer_screenshot.webp)


## ライセンス

本プロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE.txt`をご覧ください。