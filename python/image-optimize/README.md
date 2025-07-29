# image-optimize

Python スクリプトで複数画像のリサイズ・フォーマット変換を一括処理するツールです。

## 使用ライブラリ

- Python 3.x
- Pillow ライブラリ

```bash
pip install pillow
```

## 主な用途

- 画像の一括リサイズ・圧縮処理による WebP 対応
- Web サイトやブログ画像の最適化

## 使い方
### 1. リサイズ：`image_resize.py`

こちらのスクリプトでは、`input_img/` フォルダ内のすべての JPEG/PNG 画像を幅・高さともに 50% に縮小し、元の形式のまま `output_img/` に保存します。

```bash
python image_resize.py
```

出力ファイルは `<元のファイル名>` の形式になります

### 2. WebP 変換：`convert_webp.py`

こちらは JPEG/PNG を WebP フォーマット (quality=50) に変換して保存します：

```bash
python convert_webp.py
```

`output_img/` に `<元のファイル名>.webp` として出力され、

成功・エラー結果がコンソールに表示されます

## ディレクトリ構成

```
image-optimize/
├── convert_webp.py # JPEG/PNG → WebP に変換
├── image_resize.py # 画像を 50% にリサイズ
├── LICENSE.txt
├── input_img/ # 入力画像フォルダ（*.jpg, *.png）
└── output_img/ # 出力画像フォルダ（自動生成）
```

## 実行例

以下は、`image_resize.py` と `convert_webp.py` を使用した際の、画像ファイルのサイズ変化の一例です。

### 画像情報

#### 元の画像：`sample.png`

- 解像度：3024x4032
- ファイルサイズ：約5,493KB

### 実行結果

#### リサイズ後の画像（`image_resize.py` 実行後）

- 解像度：2016x1512
- ファイルサイズ：約492KB
- 削減率：約91.0%

#### WebP 形式に変換した画像（`convert_webp.py` 実行後）

- 解像度：3024x4032
- ファイルサイズ：約297KB
- 削減率：約94.6%

## ライセンス

本プロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE.txt`をご覧ください。

## 変更
### 2025‑07‑25
- `image_resize.py`で、.pngの場合の処理を変更