from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from analysis_pipeline import run_pipeline

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
    return {"message":  "running"}

@app.post("/upload")
async def upload_pitch_deck(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        
        return {"error":"Send PDF only"}
    
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    contents = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(contents)

    print("Received file:", file.filename)
    print("File size:", len(contents))

    report = run_pipeline(file_path)

    return {
        "success": True,
        "report" : report
    }