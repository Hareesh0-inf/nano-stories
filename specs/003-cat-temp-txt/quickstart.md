# Quickstart Guide

## Prerequisites
- Python 3.11+
- Node.js (for frontend development, optional)
- Gemini API key

## Backend Setup
1. Install dependencies:
   ```bash
   pip install -U google-genai>=1.32.0
   ```

2. Set environment variables:
   ```bash
   export GEMINI_API_KEY=your_api_key
   export DATABASE_URL=sqlite:///./brand_storytelling.db
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend Setup
1. Open index.html in a web browser
2. Or serve with a simple HTTP server:
   ```bash
   python -m http.server 8000
   ```

## Usage
1. Open the web application
2. Create a new project
3. Follow the 4-layer process:
   - Character: Enter details and personality
   - Product: Upload product image
   - Background: Enter scene and lighting details
   - Fusion: Enter story and generate images
4. Select from the generated images

## Testing
Run backend tests:
```bash
pytest
```
