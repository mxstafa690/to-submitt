"""
FitTrack Web Application
A simple FastAPI application that serves the frontend UI
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os

# Create FastAPI app
app = FastAPI(title="FitTrack Web App")

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main page"""
    html_path = os.path.join(BASE_DIR, "templates", "index.html")
    return FileResponse(html_path)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fittrack-web"}


if __name__ == "__main__":
    import uvicorn
    # Run the app on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
