# ベースイメージの設定
FROM python:3.8

# ワークディレクトリの設定
WORKDIR /app/backend

# 依存関係のインストール
COPY backend/requirement.txt /app/backend/
RUN pip install --no-cache-dir -r requirement.txt

# アプリケーションコードの追加
COPY backend /app/backend

# アプリケーションの起動
CMD ["uvicorn", "back:app", "--host", "0.0.0.0", "--reload"]
