# PDF生成＆日本語テキスト要約ツール

日本語テキストをPDF生成し、そのPDFから抽出した内容を `sumy` （TextRank）で要約するシンプルな Python プロジェクトです。

## 概要

- txtファイルを読み込み、日本語フォント付きのPDFを生成 
- 生成したPDFからテキストを抽出
- 抽出内容を`sumy`のTextRank要約で処理し、重要文を抽出  
- 処理結果を標準出力やファイルに出力可能  

## 内容
- `pdf_output.py` : txtファイルの文章をpdfに出力するスクリプト
- `txt_summary.py`: pdfの文章を抽出し、要約を行うスクリプト

## 依存関係

以下の Python ライブラリが必要です：

- `sumy`
- `pdfplumber`
- `fpdf2`

## 実行方法
### 1. PDF生成

```bash
python pdf_output.py
```

`txt_file.txt`を読み込んで、`japanese_txt.pdf`を生成します。

### 2. PDF読み取り＆要約

```bash
python txt_summary.py
```

PDFから日本語テキストを抽出し、要約を生成、標準出力に表示します。

## ディレクトリ構成

```
compression-files/
├── comp_7z.py      # 7z形式の圧縮スクリプト
├── comp_zip.py     # ZIP形式の圧縮スクリプト
├── NotoSansJP-Regular.ttf
├── LICENSE.txt
├── README.md
└── .gitignore
```

## フォントの準備（必須）

PDF に日本語を正しく表示するためには、**Noto Sans JP** フォントが必要です。

##### 1. [Google Fonts の Noto Sans JP ページ](https://fonts.google.com/noto/specimen/Noto%2BSans%2BJP) から `NotoSansJP-Regular.ttf` を取得してください。

##### 2. ダウンロードした `.ttf` を、**`pdf_output.py` と同じディレクトリ**に配置してください。  
- もしくは、システムフォントフォルダ（例：Windows の `C:\Windows\Fonts`）へ追加し、フォント名としてアクセス可能にしてもかまいません。

## 出力例

ChatGPTに架空のニュースを作ってもらったので、こちらの要約を行います。

### 入力（`txt_file.txt`）

```
「新型ロボット掃除機導入、地元商店街が清潔度を20％向上」

東京都小平市の小川通商店街では、地元企業と共同開発した新型ロボット掃除機を導入し、店舗前の通路清掃時間を削減しつつ、清潔度を導入前より20％向上させたと発表された。

小川通商店街振興組合（理事長：田中誠氏）が中心となり、地元のロボティクス企業「CleanTech小川」（代表取締役：佐藤由美氏）との共同プロジェクトを実施。

5月1日から、店舗前通路を自律清掃する新型ロボット掃除機「CleanBot‑X」を導入。従来の人手清掃に代わり、自動運行モードで毎朝清掃を実施。ごみの除去率は導入前比で約20％向上。

2025年5月1日より試験運用を開始し、6月末までの約2か月間で効果を計測。

東京・小平市の小川通商店街（約50店舗が加盟）。

商店街では高齢化による人手不足と衛生維持の負担を理由に、清掃作業の効率化を模索。本プロジェクトはその解決策の一環として企画。

振興組合によると、導入後の店舗スタッフの清掃負担は1日平均30分程度の削減が実現。清掃業務コストも月額約15万円減少したとのこと。佐藤社長は「さらなる性能改良やAIによる動線最適化を進め、商店街の他地域展開も視野に入れる」と述べる。

“CleanBot‑Xが導入されてから、毎朝の準備が楽になりました。スタッフ全員で喜んでいます”
— 小川通商店街 振興組合 理事 高橋美咲氏
```

### 出力（要約）

```
「新型ロボット掃除機導入、地元商店街が清潔度を20％向上」
東京都小平市の小川通商店街では、地元企業と共同開発した新型ロボット掃除機を導入し、店舗前の通路清掃時間を削減しつつ、清潔度を導入前より20％向上させたと発表された。
商店街では高齢化による人手不足と衛生維持の負担を理由に、清掃作業の効率化を模索。
振興組合によると、導入後の店舗スタッフの清掃負担は1日平均30分程度の削減が実現。
```

## 背景と経緯

元々は「PDFからテキスト抽出して要約する」だけの処理を想定していましたが、\
テキストベースのPDFの準備が意外と手間がかかったため、その部分も含めて一連の流れを自動化しました。

## ライセンス

本プロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE.txt`をご覧ください。