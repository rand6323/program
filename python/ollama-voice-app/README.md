# Ollama × VOICEVOX チャットアプリ

ローカルLLM「Ollama」と音声合成「VOICEVOX」を使った、Flask製の音声チャットアプリです。

## 特徴

- Ollamaの任意モデルでチャット
- VOICEVOXによるリアルタイム音声合成
- 設定画面からモデル・話者・速度などを変更可能
- モデル一覧は初回のみ取得しキャッシュされます

## 使用技術

- Python 3.10
- Flask
- VOICEVOX (音声合成エンジン)
- Ollama (AI モデル)

## 必要なソフトウェア

- [VOICEVOX](https://voicevox.hiroshiba.jp/)
  - VOICEVOXは、音声合成エンジンであり、音声合成のために使用しています。
  - VOICEVOXのインストール方法や使用方法については、公式サイトをご参照ください。:contentReference[oaicite:26]{index=26}

## 使用ライブラリ

- Flask
- requests
- ollama

## セットアップ

1. 必要パッケージのインストール：

```bash
pip install -r requirements.txt
```

2. VOICEVOX のパスを環境変数に設定
    1. スタートメニューを開き、「環境変数」と入力して「システム環境変数の編集」を選択します。
    2. 「システムのプロパティ」ウィンドウが開いたら、「環境変数(N)…」ボタンをクリックします。
    3. 「ユーザー環境変数」セクションで、「新規(N)…」ボタンをクリックします。
    4. 「変数名」に `VOICEVOX_PATH`、「変数値」に `C:\path\to\VOICEVOX.exe` を入力します。
    5. 「OK」をクリックしてウィンドウを閉じます。

   ※ 設定後、新しいコマンドプロンプトを開くと、設定が反映されています。
   
## 起動方法（Windows）

1. `start_app.bat` をダブルクリックしてください
2. 自動的に Flask サーバーとブラウザが起動します

## ディレクトリ構成

```
ollama-voice-app/
├── app.py
├── config.py
├── voices.py
├── start_app.bat   
├── config.json        # 初回起動後に自動生成でもOK
├── requirements.txt
├── .gitignore 
├── templates/
│   ├── index.html
│   └── settings.html
└── README.md
```

## 注意事項

- VOICEVOX / Ollama はローカルで起動されます
- audio_temp/ のWAVは自動削除されます
- config.json に設定が保存されます
- VOICEVOXを使用する際は、VOICEVOXの利用規約を遵守してください
