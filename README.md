# honto-sale-to-kindle
hontoの特設セールページの書籍を全て抜粋し、Amazonの検索結果リンクに変換する

# 準備
cp .env.default .env
.envに環境変数を記載

# 動作方法

source .env
pyenv global 3.9.5
poetry install 
python main.py
