# Audio Classification API

This project provides a FastAPI endpoint to classify audio files into three categories using Google Gemini 2.5 Flash.

## Categories
*   `0`: Surrounding description
*   `1`: Indoor Navigation
*   `2`: Outdoor navigation + destination

## Setup

1.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Ensure your `.env` file contains your `GEMINI_API_KEY`.

## Running the Server

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

**POST** `/classify-audio`
- **Body**: `file` (UploadFile)
- **Response**: JSON
  ```json
  {
      "category_id": 0,
      "category_name": "Surrounding description",
      "reasoning": "The user is asking about objects nearby."
  }
  ```

**POST** `/classify-text`
- **Body**: JSON
  ```json
  {
      "text": "Take me to the kitchen"
  }
  ```
- **Response**: JSON
  ```json
  {
      "category_id": 1,
      "category_name": "Indoor Navigation",
      "reasoning": "The user wants to go to a specific room indoors."
  }
  ```
