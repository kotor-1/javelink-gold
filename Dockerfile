FROM python:3.10-slim

# システム依存関係をインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# Pythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# ポート8080を公開（Fly.ioのデフォルト）
EXPOSE 8080

# アプリケーション起動
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
