# honto-sale-to-kindle
hontoの特設セールページの書籍を全て抜粋し、Amazonの検索結果リンクに変換する

# 準備
```
cp .env.default .env
```
.envに環境変数を記載する  
必要なもの  
- Amazon PAAPIのキー、シークレット
- bit.lyのトークン

# 動作方法
```
source .env
pyenv global 3.9.5
poetry install 
poetry shell
python main.py
```

# 実行結果
ターミナルにURLのリストが出る
```
['https://amzn.to/3peyMHW', 'https://amzn.to/3bPK2Y8', 'https://amzn.to/3vUOls4', 'https://amzn.to/3w1vg7M', 'https://amzn.to/3vYY0Ox', 'https://amzn.to/3w1vhbQ', 'https://amzn.to/3bPK3eE', 'https://amzn.to/3bN1QmK', 'https://amzn.to/3zV8obf', 'https://amzn.to/3bSr2sb', 'https://amzn.to/3pfc9Dm', 'https://amzn.to/3w0Tz5L', 'https://amzn.to/3zQwbsO', 'https://amzn.to/3zUQ3uy', 'https://amzn.to/3zT2cQJ', 'https://amzn.to/3wmN6Cr', 'https://amzn.to/3w1wjo5', 'https://amzn.to/3zNwLaJ']
```
