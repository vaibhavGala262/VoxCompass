from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from gemini_service import classify_audio, classify_text
import uuid
from pydantic import BaseModel

app = FastAPI(title="Audio Classification API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TextSubmission(BaseModel):
    text: str

@app.post("/classify-text")
async def classify_text_endpoint(submission: TextSubmission):
    """
    Classify text into:
    0: Surrounding description
    1: Indoor Navigation
    2: Outdoor navigation + destination
    """
    try:
        result = classify_text(submission.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify-audio")
async def classify_audio_endpoint(file: UploadFile = File(...)):
    """
    Upload an audio file to classify it into:
    0: Surrounding description
    1: Indoor Navigation
    2: Outdoor navigation + destination
    """
    # Generate a unique filename to avoid collisions
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        file_extension = ".mp3" # Default to mp3 if no extension
        
    temp_filename = f"{uuid.uuid4()}{file_extension}"
    temp_file_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        # Save the uploaded file locally
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the classification service
        result = classify_audio(temp_file_path)
        
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/")
def read_root():
    return {"message": "Audio and Text Classification API is running. Use POST /classify-audio or /classify-text."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
