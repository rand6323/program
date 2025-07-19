# NumberplaceGenerator

数独（ナンバープレース）の問題を自動生成し、解く Java プログラムです。

## 概要
- 完全解（ソリューション）付きの数独盤面をランダム生成  
- 指定した空白マス数になるように穴あけして、一意解になる問題に調整  
- 問題とその解答を同時にコンソールに出力  

## ディレクトリ構成
NumberplaceGeneratorProject/

├ README.md

├ src/

│   └ NumberplaceGenerator.java

└ .gitignore

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