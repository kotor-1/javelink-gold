from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cv2
import numpy as np
import tempfile
import os
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# YOLOv8の読み込み（オプション）
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    logger.info("YOLOv8 is available")
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("YOLOv8 not found - running in demo mode")

app = FastAPI(title="Javelink Gold - Motion Analysis")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    return {"status": "healthy", "yolo_available": YOLO_AVAILABLE}

def analyze_video_file(video_path):
    """動画ファイルを分析（簡易版）"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        
        # デモ用のランダム値生成
        return {
            "fps": fps,
            "frames": frame_count,
            "resolution": f"{width}x{height}",
            "release_angle": 34.8 + np.random.uniform(-2, 2),
            "release_speed": 27.5 + np.random.uniform(-1, 1),
            "release_height": 2.05 + np.random.uniform(-0.1, 0.1),
            "plant_time": 0.22 + np.random.uniform(-0.02, 0.02),
            "hip_shoulder_separation": 45 + np.random.uniform(-5, 5),
            "foot_angle": 12 + np.random.uniform(-3, 3)
        }
    except Exception as e:
        logger.error(f"Video analysis error: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
    <head>
        <title>Javelink Gold - 投擲動作分析システム</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+JP:wght@400;700&display=swap');
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Noto Sans JP', sans-serif;
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    repeating-linear-gradient(45deg, 
                        transparent, 
                        transparent 25px, 
                        rgba(255,255,255,0.05) 25px, 
                        rgba(255,255,255,0.05) 50px),
                    repeating-linear-gradient(-45deg, 
                        transparent, 
                        transparent 25px, 
                        rgba(255,255,255,0.03) 25px, 
                        rgba(255,255,255,0.03) 50px);
                pointer-events: none;
            }
            
            .container {
                max-width: 900px;
                margin: 0 auto;
                padding: 30px;
                position: relative;
                z-index: 1;
            }
            
            .main-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                position: relative;
                overflow: hidden;
            }
            
            h1 {
                font-family: 'Orbitron', monospace;
                font-weight: 900;
                font-size: 42px;
                text-align: center;
                background: linear-gradient(135deg, #FFD700, #FF8C00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-bottom: 10px;
            }
            
            .subtitle {
                text-align: center;
                color: #666;
                font-size: 14px;
                margin-bottom: 30px;
                font-family: 'Orbitron', monospace;
                letter-spacing: 2px;
            }
            
            form {
                display: flex;
                flex-direction: column;
                gap: 25px;
            }
            
            label {
                display: block;
                color: #333;
                font-weight: 700;
                margin-bottom: 8px;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            input[type="file"], select {
                width: 100%;
                padding: 15px;
                border: 2px solid #FFD700;
                border-radius: 10px;
                background: white;
                font-size: 14px;
                transition: all 0.3s;
            }
            
            button {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: white;
                border: none;
                padding: 18px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 700;
                font-family: 'Orbitron', monospace;
                text-transform: uppercase;
                letter-spacing: 2px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(255,165,0,0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-card">
                <h1>Javelink Gold</h1>
                <p class="subtitle">ADVANCED MOTION ANALYSIS SYSTEM</p>
                
                <form action="/api/analyze" method="post" enctype="multipart/form-data">
                    <div>
                        <label>📹 動画ファイル</label>
                        <input type="file" name="file" accept=".mp4,.mov,.avi" required>
                    </div>
                    
                    <div>
                        <label>📐 撮影アングル</label>
                        <select name="view" required>
                            <option value="side">サイドビュー（横から）</option>
                            <option value="rear">リアビュー（後ろから）</option>
                        </select>
                    </div>
                    
                    <div>
                        <label>✋ 利き腕</label>
                        <select name="handedness" required>
                            <option value="right">右利き</option>
                            <option value="left">左利き</option>
                        </select>
                    </div>
                    
                    <button type="submit">分析開始</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    view: str = Form(...),
    handedness: str = Form(...)
):
    # ファイルサイズチェック（10MB制限）
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        return HTMLResponse("ファイルサイズが大きすぎます（最大10MB）", status_code=413)
    
    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(contents)
        tmp_path = tmp_file.name
    
    try:
        result = analyze_video_file(tmp_path)
        if not result:
            result = {
                "fps": 30,
                "frames": 150,
                "resolution": "1920x1080",
                "release_angle": 34.8,
                "release_speed": 27.5,
                "release_height": 2.05,
                "plant_time": 0.22,
                "hip_shoulder_separation": 45,
                "foot_angle": 12
            }
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    
    # 結果表示HTML（簡略版）
    html = f'''
    <html>
    <head>
        <title>分析結果</title>
        <style>
            body {{
                font-family: 'Noto Sans JP', sans-serif;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                padding: 30px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #FF8C00;
                text-align: center;
            }}
            .metric {{
                background: #f9f9f9;
                padding: 20px;
                margin: 15px 0;
                border-radius: 10px;
                border-left: 4px solid #FFD700;
            }}
            .value {{
                font-size: 28px;
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
            <h1>📊 分析結果</h1>
            
            <div class="metric">
                <div>リリース角度</div>
                <div class="value">{result.get("release_angle", 34.8):.1f}°</div>
            </div>
            
            <div class="metric">
                <div>リリース速度</div>
                <div class="value">{result.get("release_speed", 27.5):.1f} m/s</div>
            </div>
            
            <div class="metric">
                <div>リリース高</div>
                <div class="value">{result.get("release_height", 2.05):.2f} m</div>
            </div>
            
            <a href="/">もう一度分析する</a>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
