# Audio Classification API

This project provides a FastAPI endpoint to classify audio files into three categories using Google Gemini 1.5 Flash.

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
Swagger UI documentation: `http://localhost:8000/docs`.

## Testing

You can use the provided `test_client.py` script to test the endpoint (requires an audio file).

1.  Update `test_client.py` with the path to your audio file.
2.  Run the script:
    ```bash
    python test_client.py
    ```

## API Endpoint

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
