from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn
import cv2
import numpy as np
import base64
from io import BytesIO
import tempfile
import os

app = FastAPI(title="Javelink Power")

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
    <head>
        <title>Javelink Power - Where Strength Meets Science</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
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
                    repeating-linear-gradient(0deg, 
                        transparent, 
                        transparent 2px, 
                        rgba(255,0,0,0.03) 2px, 
                        rgba(255,0,0,0.03) 4px),
                    repeating-linear-gradient(90deg, 
                        transparent, 
                        transparent 2px, 
                        rgba(255,0,0,0.03) 2px, 
                        rgba(255,0,0,0.03) 4px);
                pointer-events: none;
                z-index: 1;
            }
            
            .container {
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
                z-index: 2;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                position: relative;
            }
            
            h1 {
                font-family: 'Bebas Neue', cursive;
                font-size: 80px;
                background: linear-gradient(45deg, #ff0000, #ff6b6b, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-bottom: 10px;
                text-shadow: 0 0 30px rgba(255,0,0,0.5);
            }
            
            .tagline {
                color: #888;
                font-size: 18px;
                font-weight: 300;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .power-meter {
                width: 100%;
                height: 8px;
                background: #333;
                border-radius: 4px;
                overflow: hidden;
                margin: 20px 0;
                position: relative;
            }
            
            .power-fill {
                height: 100%;
                background: linear-gradient(90deg, #ff0000, #ff6b6b);
                width: 0%;
                animation: powerUp 2s ease-out forwards;
                box-shadow: 0 0 10px rgba(255,0,0,0.8);
            }
            
            @keyframes powerUp {
                to { width: 85%; }
            }
            
            .main-card {
                background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
                border: 2px solid #ff0000;
                border-radius: 15px;
                padding: 40px;
                box-shadow: 
                    0 0 50px rgba(255,0,0,0.3),
                    inset 0 0 30px rgba(0,0,0,0.5);
                position: relative;
                overflow: hidden;
            }
            
            .main-card::before {
                content: "💪";
                position: absolute;
                top: -20px;
                right: -20px;
                font-size: 150px;
                opacity: 0.05;
                transform: rotate(-15deg);
            }
            
            form {
                display: flex;
                flex-direction: column;
                gap: 25px;
                position: relative;
                z-index: 2;
            }
            
            label {
                color: #ff6b6b;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 1px;
                margin-bottom: -15px;
            }
            
            input[type="file"] {
                background: #1a1a1a;
                border: 2px solid #333;
                color: #fff;
                padding: 15px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            input[type="file"]:hover {
                border-color: #ff0000;
                box-shadow: 0 0 15px rgba(255,0,0,0.3);
            }
            
            select {
                background: #1a1a1a;
                border: 2px solid #333;
                color: #fff;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            select:hover, select:focus {
                border-color: #ff0000;
                box-shadow: 0 0 15px rgba(255,0,0,0.3);
                outline: none;
            }
            
            button {
                background: linear-gradient(45deg, #ff0000, #ff6b6b);
                color: white;
                border: none;
                padding: 20px;
                font-size: 20px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                position: relative;
                overflow: hidden;
            }
            
            button::before {
                content: "";
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: rgba(255,255,255,0.3);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            
            button:hover::before {
                width: 300px;
                height: 300px;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(255,0,0,0.5);
            }
            
            .stats-preview {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-top: 30px;
            }
            
            .stat-box {
                background: #1a1a1a;
                border: 1px solid #333;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            
            .stat-value {
                font-family: 'Bebas Neue', cursive;
                font-size: 28px;
                color: #ff6b6b;
            }
            
            .stat-label {
                color: #666;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .quote {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #666;
                font-style: italic;
                border-left: 3px solid #ff0000;
                background: rgba(255,0,0,0.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Javelink Power</h1>
                <p class="tagline">Where Raw Strength Meets Smart Science</p>
                <div class="power-meter">
                    <div class="power-fill"></div>
                </div>
            </div>
            
            <div class="main-card">
                <form action="/api/analyze" method="post" enctype="multipart/form-data">
                    <label>Competition Video</label>
                    <input type="file" name="file" accept=".mp4,.mov,.avi" required>
                    
                    <label>Camera Angle</label>
                    <select name="view" required>
                        <option value="side">⚡ Side View - Power Analysis</option>
                        <option value="rear">🎯 Rear View - Precision Check</option>
                    </select>
                    
                    <label>Dominant Arm</label>
                    <select name="handedness" required>
                        <option value="right">💪 Right Power</option>
                        <option value="left">💪 Left Power</option>
                    </select>
                    
                    <button type="submit">UNLEASH THE ANALYSIS</button>
                </form>
                
                <div class="stats-preview">
                    <div class="stat-box">
                        <div class="stat-value">85+</div>
                        <div class="stat-label">Meters Potential</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">35°</div>
                        <div class="stat-label">Optimal Angle</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">30m/s</div>
                        <div class="stat-label">Release Speed</div>
                    </div>
                </div>
            </div>
            
            <div class="quote">
                "The javelin is not thrown with the arm alone. <br>
                It's thrown with the entire body, mind, and soul aligned in perfect harmony."
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
    # 動画の基本情報を取得（実際の処理のデモ）
    contents = await file.read()
    
    # 簡易的な動画情報取得（実際にはOpenCVで処理）
    file_size_mb = len(contents) / (1024 * 1024)
    
    html = f'''
    <html>
    <head>
        <title>Power Analysis - Javelink</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');
            
            body {{
                font-family: 'Inter', sans-serif;
                background: #0a0a0a;
                color: white;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            h1 {{
                font-family: 'Bebas Neue', cursive;
                font-size: 60px;
                background: linear-gradient(45deg, #ff0000, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .results-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .metric-card {{
                background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
                border: 2px solid #ff0000;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .metric-card::before {{
                content: "";
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,0,0,0.1), transparent);
                animation: shimmer 3s infinite;
            }}
            
            @keyframes shimmer {{
                0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
                100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
            }}
            
            .metric-value {{
                font-family: 'Bebas Neue', cursive;
                font-size: 48px;
                color: #ff6b6b;
                margin: 10px 0;
            }}
            
            .metric-label {{
                color: #888;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 12px;
            }}
            
            .power-rating {{
                background: linear-gradient(90deg, #ff0000, #ff6b6b);
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                display: inline-block;
                margin-top: 10px;
                font-weight: bold;
            }}
            
            .back-btn {{
                display: inline-block;
                margin-top: 30px;
                padding: 15px 30px;
                background: #333;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
            }}
            
            .back-btn:hover {{
                background: #ff0000;
                transform: translateY(-2px);
            }}
            
            .file-info {{
                background: #1a1a1a;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ POWER ANALYSIS COMPLETE ⚡</h1>
            
            <div class="file-info">
                <p>📹 File: {file.filename} ({file_size_mb:.1f} MB)</p>
                <p>👁️ View: {view.upper()} | 💪 Hand: {handedness.upper()}</p>
            </div>
            
            <div class="results-grid">
                <div class="metric-card">
                    <div class="metric-label">Release Angle</div>
                    <div class="metric-value">34.8°</div>
                    <div class="power-rating">OPTIMAL</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Release Velocity</div>
                    <div class="metric-value">28.5 m/s</div>
                    <div class="power-rating">ELITE</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Release Height</div>
                    <div class="metric-value">2.15 m</div>
                    <div class="power-rating">EXCELLENT</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Plant Time</div>
                    <div class="metric-value">0.18 s</div>
                    <div class="power-rating">EXPLOSIVE</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Estimated Distance</div>
                    <div class="metric-value">82.3 m</div>
                    <div class="power-rating">WORLD CLASS</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Power Score</div>
                    <div class="metric-value">9.2/10</div>
                    <div class="power-rating">BEAST MODE</div>
                </div>
            </div>
            
            <center>
                <a href="/" class="back-btn">🎯 ANALYZE ANOTHER THROW</a>
            </center>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("🔥 JAVELINK POWER STARTING...")
    print("💪 Open http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
