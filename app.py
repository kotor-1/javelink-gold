from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import os
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Javelink Gold - Motion Analysis")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ヘルスチェック
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Javelink Gold"}

def analyze_video_demo(filename: str):
    """デモ用の分析結果を生成"""
    # ランダムな値を生成（デモ用）
    return {
        "filename": filename,
        "fps": 30,
        "frames": 150,
        "resolution": "1920x1080",
        "release_angle": 34.8 + np.random.uniform(-2, 2),
        "release_speed": 27.5 + np.random.uniform(-1, 1),
        "release_height": 2.05 + np.random.uniform(-0.1, 0.1),
        "plant_time": 0.22 + np.random.uniform(-0.02, 0.02),
        "hip_shoulder_separation": 45 + np.random.uniform(-5, 5),
        "foot_angle": 12 + np.random.uniform(-3, 3)
    }

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head>
        <title>Javelink Gold</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 90%;
            }
            h1 {
                color: #FF8C00;
                text-align: center;
                margin-bottom: 30px;
                font-size: 32px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            label {
                color: #333;
                font-weight: bold;
            }
            input, select {
                padding: 12px;
                border: 2px solid #FFD700;
                border-radius: 8px;
                font-size: 14px;
            }
            button {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Javelink Gold</h1>
            <form action="/api/analyze" method="post" enctype="multipart/form-data">
                <div>
                    <label>動画ファイル</label>
                    <input type="file" name="file" accept=".mp4,.mov,.avi" required>
                </div>
                <div>
                    <label>撮影アングル</label>
                    <select name="view" required>
                        <option value="side">横から</option>
                        <option value="rear">後ろから</option>
                    </select>
                </div>
                <div>
                    <label>利き腕</label>
                    <select name="handedness" required>
                        <option value="right">右</option>
                        <option value="left">左</option>
                    </select>
                </div>
                <button type="submit">分析開始</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    view: str = Form(...),
    handedness: str = Form(...)
):
    # ファイルサイズチェック
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        return HTMLResponse("<h1>ファイルが大きすぎます（最大10MB）</h1>", status_code=413)
    
    # デモ分析を実行
    result = analyze_video_demo(file.filename)
    
    # 結果表示
    html = f"""
    <html>
    <head>
        <title>分析結果</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 20px;
            }}
            h1 {{
                color: #FF8C00;
                text-align: center;
                margin-bottom: 30px;
            }}
            .metric {{
                background: #f9f9f9;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #FFD700;
            }}
            .label {{
                color: #666;
                font-size: 14px;
            }}
            .value {{
                font-size: 24px;
                color: #FF8C00;
                font-weight: bold;
            }}
            a {{
                display: block;
                text-align: center;
                margin-top: 30px;
                padding: 15px;
                background: #FFD700;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>分析結果</h1>
            <p style="text-align: center; color: #666;">ファイル: {result["filename"]}</p>
            
            <div class="metric">
                <div class="label">リリース角度</div>
                <div class="value">{result["release_angle"]:.1f}°</div>
            </div>
            
            <div class="metric">
                <div class="label">リリース速度</div>
                <div class="value">{result["release_speed"]:.1f} m/s</div>
            </div>
            
            <div class="metric">
                <div class="label">リリース高</div>
                <div class="value">{result["release_height"]:.2f} m</div>
            </div>
            
            <div class="metric">
                <div class="label">ブロック時間</div>
                <div class="value">{result["plant_time"]:.2f} 秒</div>
            </div>
            
            <a href="/">もう一度分析</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)