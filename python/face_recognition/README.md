# 顔認証アプリ

OpenCVを使って、PC上で単一人物の顔認識を行うPythonアプリです。

## 概要
OpenCV の LBPH（Local Binary Pattern Histogram）を使った単一人物顔認証アプリ。  
顔画像を収集・学習し、画像やカメラ映像でリアルタイム認識できます。

## 使用技術
Python 3.11

OpenCV（opencv-contrib-python）

NumPy

## 機能
- capture.py: カメラ映像からキー入力で顔を収集
- detect: 顔検出と切り出し、detected/に保存
- train.py: 切り出し画像でモデルを学習し、models/face_recognizer.ymlを生成
- recognize.py: 画像またはWebカメラ映像から顔認識（矩形＋confidence表示）

## ディレクトリ構成

```
face_recognition/
├ input/                  # カメラ撮影または画像選択した未処理の顔画像
├ detected/              # detect.pyで切り出した顔部分
├ models/
│   └ face_recognizer.yml  # 学習済モデル
├ test/                  # 認識テスト用の画像（サンプル含む）
├ capture.py             # 顔画像収集スクリプト
├ detect.py              # 顔検出＆切り出しスクリプト
├ train.py               # 学習処理スクリプト
├ recognize.py           # 画像・リアルタイム顔認識スクリプト
├ requirements.txt       # 必要パッケージ一覧
└ README.md              # 本ドキュメント
```

## セットアップ
```
git clone https://github.com/rand6323/progrram/face_recognition
cd face_recognition
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 使い方

### 1. 顔画像収集（Webカメラ）
```
python capture.py
```
'c'キーで撮影・保存、'q'キーで終了。

### 2. 顔検出・切り出し
```
python detect.py
```
input/フォルダ内の画像から顔検出し、detected/フォルダに保存。

### 3. モデル学習
```
python train.py
```
input/フォルダ内の画像から顔を検出・切り出し、LBPHモデルに学習させて models/face_recognizer.yml として保存。

### 4. 顔認識
```
python recognize.py
```
Webカメラからの映像をリアルタイムで取得し、事前に学習した顔認識モデルを用いて顔を検出・認識し、認識結果を画面上に表示。
