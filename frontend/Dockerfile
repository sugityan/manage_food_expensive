# ベースイメージの設定
FROM node:14

# ワークディレクトリの設定
WORKDIR /app/frontend

# 依存関係のインストール
COPY frontend/package*.json ./
RUN npm install

# アプリケーションコードの追加
COPY frontend /app/frontend

# アプリケーションの起動
CMD ["npm", "start"]
