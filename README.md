# Javelink Gold - 投擲動作分析システム

AIを使用したやり投げ動作の科学的分析アプリケーション

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9+-red)
![YOLOv8](https://img.shields.io/badge/YOLOv8-pose-purple)

## 🎯 特徴

- **リアルタイム動画分析**: OpenCV + YOLOv8による姿勢検出
- **6つの重要指標**: リリース角度、速度、高さなどを自動計測
- **わかりやすい解説**: 小中高生でも理解できる説明付き
- **美しいUI**: ゴールド×オレンジの未来的デザイン

## 📊 測定項目

1. **リリース角度** - やりを投げる瞬間の角度
2. **リリース速度** - やりが手から離れる速さ
3. **リリース高** - リリース時の地面からの高さ
4. **ブロック時間** - 最後の一歩から投げるまでの時間
5. **肩腰分離角** - 体のねじれ具合
6. **前足進行角** - 踏み込み足の向き

## 🚀 クイックスタート

### 必要環境
- Python 3.10以上
- FFmpeg（動画処理用）

### インストール

\\\ash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/javelink-gold.git
cd javelink-gold

# 仮想環境を作成
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
\\\

### 実行

\\\ash
python javelink_gold.py
\\\

ブラウザで http://localhost:8000 にアクセス

## 🌐 デプロイ

### Render.com でのデプロイ

1. [Render.com](https://render.com) でアカウント作成
2. New > Web Service を選択
3. GitHubリポジトリを接続
4. 以下の設定を使用:
   - **Environment**: Python 3
   - **Build Command**: pip install -r requirements.txt
   - **Start Command**: uvicorn app:app --host 0.0.0.0 --port 

### Railway でのデプロイ

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 📁 プロジェクト構造

\\\
javelink-gold/
├── javelink_gold.py    # メインアプリケーション
├── requirements.txt    # 依存関係
├── README.md          # このファイル
├── .gitignore         # Git除外設定
└── Procfile           # Heroku/Railway用
\\\

## 🛠️ 技術スタック

- **バックエンド**: FastAPI, Python
- **画像処理**: OpenCV, NumPy
- **AI/ML**: YOLOv8 (Ultralytics)
- **フロントエンド**: HTML5, CSS3, JavaScript

## 📝 ライセンス

MIT License

## 🤝 貢献

Issues や Pull Requests を歓迎します！

## 📧 お問い合わせ

質問や提案は [Issues](https://github.com/YOUR_USERNAME/javelink-gold/issues) まで

---

Made with ❤️ for javelin throwers
