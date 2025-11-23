import requests
import os
import time
from gtts import gTTS

OUTPUT_FILE = "result.txt"

def log(message):
    print(message)
    with open(OUTPUT_FILE, "a") as f:
        f.write(str(message) + "\n")

def generate_audio(text, filename):
    log(f"Generating audio for: '{text}' -> {filename}")
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def test_classification(filename, expected_cat):
    url = "http://localhost:8000/classify-audio"
    
    if not os.path.exists(filename):
        log(f"Error: File {filename} not found.")
        return

    log(f"\n--- Testing {filename} ---")
    log(f"Expected Category: {expected_cat}")
    
    try:
        with open(filename, "rb") as f:
            files = {"file": f}
            start_time = time.time()
            response = requests.post(url, files=files)
            duration = time.time() - start_time
            
        if response.status_code == 200:
            result = response.json()
            log(f"Time: {duration:.2f}s")
            log(f"Result: {result}")
            
            # Simple verification
            if result.get('category_id') == expected_cat:
                log("PASS")
            else:
                log(f"FAIL (Expected {expected_cat}, got {result.get('category_id')})")
        else:
            log(f"Failed with status code: {response.status_code}")
            log(response.text)
            
    except Exception as e:
        log(f"An error occurred: {e}")

def main():
    # Clear previous results
    with open(OUTPUT_FILE, "w") as f:
        f.write("Test Results\n============\n")

    # Define test cases
    test_cases = [
        {
            "text": "What is around me? Describe the surroundings.",
            "file": "test_cat_0.mp3",
            "expected": 0
        },
        {
            "text": "Take me to the kitchen please.",
            "file": "test_cat_1.mp3",
            "expected": 1
        },
        {
            "text": "Navigate to the nearest Starbucks.",
            "file": "test_cat_2.mp3",
            "expected": 2
        }
    ]

    log("1. Generating Audio Files...")
    for case in test_cases:
        generate_audio(case["text"], case["file"])

    log("\n2. Running Tests...")
    for case in test_cases:
        test_classification(case["file"], case["expected"])
        
    log("\nDone.")

if __name__ == "__main__":
    main()
