# NumberplaceGenerator

数独（ナンバープレース）の問題を自動生成し、解く Java プログラムです。

## 概要
- 完全解（ソリューション）付きの数独盤面をランダム生成  
- 指定した空白マス数になるように穴あけして、一意解になる問題に調整  
- 問題とその解答を同時にコンソールに出力  

## ディレクトリ構成

```
NumberplaceGeneratorProject/
├── README.md
├── src/
│       └ NumberplaceGenerator.java
├── LICENSE.txt
├── .gitignore
```

## 起動方法

### 1. Java がインストールされていることを確認  
```
java -version
```

### 2. ソースをコンパイル
```
javac src/NumberplaceGenerator.java
```

### 3. プログラムを実行
```
java -cp src NumberplaceGenerator
```
実行時の blanks（空白マス）数は main() 内で変更可能（デフォルトは50）。


## 基本ロジック解説
- generateFullSolvedSudoku(): ランダムに完全解盤面を生成

- generateUniqueProblemFromSolution(...): 解が一意になるように空白マスを設定

- countSolutionsLimited(...): 解の数を最大2つまで確認し、多解を検出

- printBoard(...): Console に盤面を整形して出力

更に詳細なコメントはコード中に Javadoc やインラインコメントで追加済みです。

## 出力例

- 問題例
以下は、生成される数独の問題の一例です：

```
■ 問題:
[0, 0, 0, 5, 7, 8, 0, 0, 2]
[0, 0, 0, 4, 0, 0, 6, 0, 0]
[0, 9, 0, 3, 0, 0, 0, 7, 0]
[0, 0, 0, 0, 0, 0, 2, 0, 6]
[0, 5, 0, 0, 3, 6, 0, 4, 9]
[0, 6, 2, 9, 0, 5, 7, 3, 8]
[5, 0, 4, 0, 0, 0, 0, 6, 0]
[0, 0, 9, 0, 0, 0, 4, 8, 0]
[0, 0, 0, 8, 9, 0, 0, 0, 0]
```

- 解答例
上記の問題に対する解答は以下の通りです：

```
■ 解答:
[4, 1, 6, 5, 7, 8, 3, 9, 2]
[3, 7, 8, 4, 2, 9, 6, 1, 5]
[2, 9, 5, 3, 6, 1, 8, 7, 4]
[9, 4, 3, 1, 8, 7, 2, 5, 6]
[8, 5, 7, 2, 3, 6, 1, 4, 9]
[1, 6, 2, 9, 4, 5, 7, 3, 8]
[5, 8, 4, 7, 1, 2, 9, 6, 3]
[7, 2, 9, 6, 5, 3, 4, 8, 1]
[6, 3, 1, 8, 9, 4, 5, 2, 7]
```

## ライセンス

本プロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE.txt`をご覧ください。