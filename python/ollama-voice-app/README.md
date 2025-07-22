# Ollama × VOICEVOX チャットアプリ

ローカルLLM「Ollama」と音声合成「VOICEVOX」を使った、Flask製の音声チャットアプリです。

## 特徴

- Ollamaの任意モデルでチャット
- VOICEVOXによるリアルタイム音声合成
- 設定画面からモデル・話者・速度などを変更可能
- モデル一覧は初回のみ取得しキャッシュされます

## 使用ライブラリ

- Flask
- requests
- ollama

## セットアップ

1. 必要パッケージのインストール：

```bash
pip install -r requirements.txt
```

2. VOICEVOX のパスを環境変数に設定（例：Windows）

```bash
setx VOICEVOX_PATH "C:\path\to\VOICEVOX.exe"
```
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
