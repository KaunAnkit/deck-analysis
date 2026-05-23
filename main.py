from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from analysis_pipeline import run_pipeline

from cold_mail.pipeline import generate_cold_email

import json



import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "running"}

@app.post("/upload")
async def upload_pitch_deck(
    file: UploadFile = File(...),
    deck_goal: str = Form(...),
    deck_type: str = Form(...),
    fund_size: str = Form(""),
    growth_focus: str = Form(""),
    deck_timeline: str = Form("")
):

    if not file.filename.endswith(".pdf"):
        return {"error": "Send PDF only"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    deck_context = {
        "deck_goal": deck_goal,
        "deck_type": deck_type,
        "fund_size": fund_size,
        "growth_focus": growth_focus,
        "deck_timeline": deck_timeline
    }

    result = run_pipeline(file_path, deck_context)

    return {
        "success": True,
        "report": result["report"],
        "startup_profile":result["startup_profile"]
    }


@app.post("/generate-email")
async def generate_email_endpoint(
    linkedin_url: str = Form(...),
    startup_profile: str = Form(...)
):

    startup_profile = json.loads(
        startup_profile
    )

    email = generate_cold_email(
        linkedin_url,
        startup_profile
    )

    return {
        "success": True,
        "email": email
    }