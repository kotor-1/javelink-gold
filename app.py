from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI(title="Javelink Gold")

@app.get("/")
async def root():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Javelink Gold</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                min-height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 500px;
                width: 90%;
            }
            h1 {
                color: #FF8C00;
                text-align: center;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            input, select, button {
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #FFD700;
                font-size: 14px;
            }
            button {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: white;
                border: none;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Javelink Gold</h1>
            <p style="text-align: center; color: #666;">投擲動作分析システム</p>
            <form action="/analyze" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".mp4,.mov,.avi" required>
                <select name="view" required>
                    <option value="side">横から撮影</option>
                    <option value="rear">後ろから撮影</option>
                </select>
                <select name="handedness" required>
                    <option value="right">右利き</option>
                    <option value="left">左利き</option>
                </select>
                <button type="submit">分析開始</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    view: str = Form(...),
    handedness: str = Form(...)
):
    # デモ結果を返す
    html_content = f'''
    <!DOCTYPE html>
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
            }}
            .metric {{
                background: #f9f9f9;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border-left: 4px solid #FFD700;
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
            <p style="text-align: center;">ファイル: {file.filename}</p>
            <div class="metric">
                <div>リリース角度</div>
                <div class="value">34.8°</div>
            </div>
            <div class="metric">
                <div>リリース速度</div>
                <div class="value">27.5 m/s</div>
            </div>
            <div class="metric">
                <div>リリース高</div>
                <div class="value">2.05 m</div>
            </div>
            <a href="/">もう一度分析</a>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
