# ai_interviewer/api/main.py

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from ai_interviewer.api import routes

# --- Path Setup ---
# This code figures out where your frontend/index.html file is located
# relative to this main.py file, making it work reliably.
API_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(API_DIR, "..", ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "ai_interviewer/frontend")


# Create the main FastAPI application instance
app = FastAPI(
    title="AI Interviewer API",
    description="Real-time technical interviews with an AI.",
    version="3.0"
)

# Include the WebSocket router from the routes module.
app.include_router(routes.router)


@app.get("/")
async def serve_frontend():
    """
    This endpoint serves your main index.html file when someone visits
    the root URL of the server.
    """
    html_file_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path)
    return {"error": "index.html not found. Please ensure the frontend directory is correctly placed."}

