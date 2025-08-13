from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Javelink Lite")

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
    <head>
        <title>Javelink Lite</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #333; text-align: center; }
            form { display: flex; flex-direction: column; gap: 15px; }
            input, select, button { padding: 10px; font-size: 16px; }
            button { background: #007bff; color: white; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Javelink Lite</h1>
            <p style="text-align: center;">Upload your throwing motion video for analysis</p>
            <form action="/api/analyze" method="post" enctype="multipart/form-data">
                <label>Video File:</label>
                <input type="file" name="file" accept=".mp4,.mov,.avi" required>
                
                <label>Camera View:</label>
                <select name="view" required>
                    <option value="side">Side View</option>
                    <option value="rear">Rear View</option>
                </select>
                
                <label>Throwing Hand:</label>
                <select name="handedness" required>
                    <option value="right">Right Hand</option>
                    <option value="left">Left Hand</option>
                </select>
                
                <button type="submit">Start Analysis</button>
            </form>
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
    # Demo results
    html = f'''
    <html>
    <head>
        <title>Results - Javelink Lite</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #f0f0f0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            h1 {{ color: #333; }}
            .metric {{ background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .value {{ font-size: 24px; color: #007bff; font-weight: bold; }}
            a {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Analysis Complete!</h1>
            <p>File: {file.filename}</p>
            <p>View: {view} / Hand: {handedness}</p>
            
            <h2>Results (Demo)</h2>
            <div class="metric">
                <div>Release Angle</div>
                <div class="value">35.5°</div>
            </div>
            <div class="metric">
                <div>Release Speed</div>
                <div class="value">18.3 m/s</div>
            </div>
            <div class="metric">
                <div>Release Height</div>
                <div class="value">1.92 m</div>
            </div>
            
            <a href="/">New Analysis</a>
        </div>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("Starting Javelink Lite...")
    print("Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
