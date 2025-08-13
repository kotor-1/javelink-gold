from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn
import os
import io
import base64
from PIL import Image
import numpy as np

# メモリ節約設定
import torch
torch.set_num_threads(1)

app = FastAPI(title="Javelink YOLO Lite")

# グローバル変数でモデルを保持（初回のみロード）
model = None

def get_model():
    global model
    if model is None:
        try:
            from ultralytics import YOLO
            # 最軽量のnanoモデルを使用
            model = YOLO('yolov8n-pose.pt')
            print("YOLOv8n loaded successfully")
        except Exception as e:
            print(f"Failed to load YOLO: {e}")
            model = "failed"
    return model

def analyze_image(image_bytes):
    """画像から姿勢を検出（最小処理）"""
    try:
        # モデル取得
        yolo_model = get_model()
        if yolo_model == "failed" or yolo_model is None:
            return None
        
        # PILで画像を開く
        image = Image.open(io.BytesIO(image_bytes))
        
        # サイズを縮小（メモリ節約）
        max_size = 640
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size))
        
        # YOLO推論（1フレームのみ）
        results = yolo_model(image, verbose=False)
        
        if results and len(results) > 0:
            # キーポイントを取得
            if results[0].keypoints is not None:
                keypoints = results[0].keypoints.data
                if len(keypoints) > 0:
                    # 簡単な計算（肩と腰の角度など）
                    kp = keypoints[0].cpu().numpy()
                    
                    # 肩の角度を計算（例）
                    if kp[5][2] > 0.5 and kp[6][2] > 0.5:  # 信頼度チェック
                        shoulder_angle = np.arctan2(
                            kp[6][1] - kp[5][1],
                            kp[6][0] - kp[5][0]
                        )
                        return {
                            "detected": True,
                            "angle": float(np.degrees(shoulder_angle)),
                            "confidence": float(kp[5][2])
                        }
        
        return {"detected": False}
    
    except Exception as e:
        print(f"Analysis error: {e}")
        return None

@app.get("/")
async def root():
    return HTMLResponse('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Javelink YOLO Lite</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 500px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .status {
                text-align: center;
                padding: 10px;
                background: #f0f0f0;
                border-radius: 10px;
                margin: 20px 0;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            input, button {
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #ddd;
                font-size: 16px;
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background: #5a67d8;
            }
            .warning {
                background: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Javelink YOLO Lite</h1>
            <div class="status">YOLOv8n 最軽量版</div>
            
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <button type="submit">画像を分析</button>
            </form>
            
            <div class="warning">
                ⚠️ メモリ制限のため、画像のみ対応（動画は非対応）
            </div>
        </div>
    </body>
    </html>
    ''')

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # ファイルサイズ制限（2MB）
    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:
        return HTMLResponse("<h1>ファイルが大きすぎます（最大2MB）</h1>")
    
    # 画像分析
    result = analyze_image(contents)
    
    # 結果表示
    if result and result.get("detected"):
        status = "✅ 姿勢検出成功"
        details = f"""
        <div style='background: #d4edda; padding: 20px; border-radius: 10px; color: #155724;'>
            <h3>検出結果</h3>
            <p>肩の角度: {result.get('angle', 0):.1f}°</p>
            <p>信頼度: {result.get('confidence', 0):.2%}</p>
        </div>
        """
    else:
        status = "❌ 姿勢検出失敗"
        details = "<p>人物が検出できませんでした</p>"
    
    return HTMLResponse(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>分析結果</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                padding: 20px;
            }}
            .container {{
                max-width: 500px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            a {{
                display: block;
                text-align: center;
                margin-top: 20px;
                padding: 12px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{status}</h1>
            {details}
            <a href="/">もう一度試す</a>
        </div>
    </body>
    </html>
    ''')

@app.get("/health")
async def health():
    model_status = "not_loaded"
    try:
        m = get_model()
        if m != "failed" and m is not None:
            model_status = "loaded"
    except:
        pass
    
    return {
        "status": "healthy",
        "model": model_status,
        "memory_limit": "512MB"
    }

if __name__ == "__main__":
    # 起動時にモデルをロード
    print("Loading YOLOv8n model...")
    get_model()
    
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
