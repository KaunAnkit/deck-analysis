from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Backend running"}

@app.post("/upload")
async def upload_pitch_deck(file: UploadFile = File(...)):

    contents = await file.read()

    print("Received file:", file.filename)
    print("File size:", len(contents))

    return {
        "success": True,
        "filename": file.filename,
        "size": len(contents)
    }