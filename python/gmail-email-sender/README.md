# Gmail APIで添付付きメール送信（Python）

任意の形式（`.pdf`、`.zip`、`.jpg`、`.xls` 等）の添付ファイルを含むメールを Gmail API経由で送信する Pythonスクリプトの使い方を示します。

## 前提条件
- Python 3.x
- `credentials.json`（OAuthクライアントID）
- Gmail API有効化済みGoogle Cloudプロジェクト
- 以下の Python パッケージをインストールしてください：
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Gmail APIの有効化とOAuth設定

##### 1. Google Cloud Consoleでプロジェクトを作成または選択
##### 2.「APIs&Services > Library」からGmail APIを有効化
##### 3.「OAuth同意画面」でアプリ情報とテストユーザーを設定
##### 4.「Credentials」でOAuthクライアントIDを作成し、`credentials.json`をダウンロード
- このファイルをリポジトリのルートに配置します

## ディレクトリ構成

```
email_/
├── send_mail.py       # メール送信スクリプト
├── README.md          # このファイル
├── LICENSE.txt
└── .gitignore
```

## ライセンス

本プロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE.txt`をご覧ください。