import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=API_KEY)

def classify_audio(audio_file_path: str):
    """
    Uploads an audio file to Gemini and classifies it.
    """
    try:
        # 1. Upload the file
        print(f"Uploading file: {audio_file_path}...")
        audio_file = genai.upload_file(path=audio_file_path)
        
        # Wait for the file to be processed
        # Optimized polling: check every 0.2s instead of 1s
        while audio_file.state.name == "PROCESSING":
            # print("Processing audio file...") 
            time.sleep(0.2)
            audio_file = genai.get_file(audio_file.name)

        if audio_file.state.name == "FAILED":
            raise ValueError("Audio file processing failed.")

        print(f"File uploaded: {audio_file.uri}")

        # 2. Initialize Model
        # Using gemini-1.5-flash (8b was not found)
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        print(f"DEBUG: Initialized model with name: {model.model_name}")

        # 3. Generate Content
        prompt = """
        Listen to this audio clip carefully. It contains a spoken command or description.
        Classify the intent into exactly one of these three categories:

        0: Surrounding description (e.g., "There is a table in front of me", "What is around me?")
        1: Indoor Navigation (e.g., "Take me to the kitchen", "Where is the bathroom?", "Go to room 101")
        2: Outdoor navigation + destination (e.g., "Navigate to Starbucks", "Take me to Central Park", "Directions to the nearest hospital")

        Return ONLY a JSON object with the following format, no other text:
        {
            "category_id": <int>,
            "category_name": "<string>",
            "reasoning": "<short explanation>"
        }
        """

        response = model.generate_content([prompt, audio_file])
        
        # 4. Parse Response
        response_text = response.text.strip()
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text)
        
        # Cleanup: Delete the file from Gemini storage to avoid clutter
        # genai.delete_file(audio_file.name) 
        
        return result

    except Exception as e:
        print(f"Error in classify_audio: {e}")
        raise e
