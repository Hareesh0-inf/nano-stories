# Brand Storytelling API Documentation

## Overview
The Brand Storytelling API provides endpoints for creating and managing brand storytelling projects with AI-powered image generation using Google's Gemini API.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API uses environment-based authentication with the `GEMINI_API_KEY` environment variable.

## Endpoints

### Projects

#### Create Project
**POST** `/projects`

Creates a new brand storytelling project.

**Request Body:**
```json
{
  "name": "My Brand Story Project"
}
```

**Response:**
```json
{
  "id": "1",
  "name": "My Brand Story Project",
  "created_at": "2025-09-07T10:00:00Z"
}
```

**Status Codes:**
- `201` - Project created successfully
- `422` - Invalid project name

### Characters

#### Generate Character Image
**POST** `/projects/{project_id}/character`

Generates a character image based on provided details and personality.

**Request Body:**
```json
{
  "details": "A professional business person in a modern office",
  "personality": "confident and approachable"
}
```

**Response:**
```json
{
  "id": "1",
  "image_url": "https://example.com/generated-character.jpg"
}
```

**Status Codes:**
- `200` - Character image generated successfully
- `404` - Project not found
- `422` - Invalid character details

### Products

#### Upload Product Image
**POST** `/projects/{project_id}/product`

Uploads and stores a product image for the project.

**Request Body (Form Data):**
- `file`: Product image file (JPEG, PNG, etc.)
- `filename`: Optional custom filename

**Response:**
```json
{
  "id": "1",
  "filename": "product_image.jpg",
  "content_type": "image/jpeg",
  "image_url": "/uploads/products/product_image.jpg"
}
```

**Status Codes:**
- `201` - Product uploaded successfully
- `404` - Project not found
- `422` - Invalid file format

### Backgrounds

#### Generate Background Image
**POST** `/projects/{project_id}/background`

Generates a background scene image based on scene details and lighting preferences.

**Request Body:**
```json
{
  "scene_details": "Modern corporate office with large windows",
  "lighting": "natural daylight"
}
```

**Response:**
```json
{
  "id": "1",
  "image_url": "https://example.com/generated-background.jpg"
}
```

**Status Codes:**
- `200` - Background image generated successfully
- `404` - Project not found
- `422` - Invalid scene details

### Stories

#### Create Story
**POST** `/projects/{project_id}/story`

Creates a story element for the brand storytelling project.

**Request Body:**
```json
{
  "story_text": "A compelling narrative about innovation and growth"
}
```

**Response:**
```json
{
  "id": "1",
  "story_text": "A compelling narrative about innovation and growth"
}
```

**Status Codes:**
- `201` - Story created successfully
- `404` - Project not found
- `422` - Invalid story text

### Image Generation

#### Generate Final Images
**POST** `/projects/{project_id}/generate`

Generates final brand storytelling images by combining character, product, background, and story elements.

**Request Body:**
```json
{
  "fusion_style": "professional",
  "num_images": 3
}
```

**Response:**
```json
{
  "images": [
    {
      "id": "1",
      "prompt": "Professional brand story image combining character, product, and background",
      "image_url": "https://example.com/final-image-1.jpg",
      "fusion_style": "professional"
    },
    {
      "id": "2",
      "prompt": "Creative brand story image with modern aesthetic",
      "image_url": "https://example.com/final-image-2.jpg",
      "fusion_style": "professional"
    }
  ]
}
```

**Status Codes:**
- `200` - Images generated successfully
- `404` - Project not found or missing required elements
- `422` - Invalid generation parameters

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Error description message"
}
```

## Rate Limiting

The API implements rate limiting based on the Gemini API quotas:
- Character generation: Limited by API quota
- Background generation: Limited by API quota
- Final image generation: Limited by API quota

## File Upload Limits

- Maximum file size: 10MB
- Supported formats: JPEG, PNG, GIF, WebP
- Upload directory: `/uploads/products/`

## Data Models

### Project
```json
{
  "id": "integer",
  "name": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Character
```json
{
  "id": "integer",
  "project_id": "integer",
  "details": "string",
  "personality": "string",
  "image_url": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Product
```json
{
  "id": "integer",
  "project_id": "integer",
  "image_url": "string",
  "filename": "string",
  "content_type": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Background
```json
{
  "id": "integer",
  "project_id": "integer",
  "scene_details": "string",
  "lighting": "string",
  "image_url": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Story
```json
{
  "id": "integer",
  "project_id": "integer",
  "story_text": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Image
```json
{
  "id": "integer",
  "project_id": "integer",
  "prompt": "string",
  "image_url": "string",
  "image_type": "string",
  "fusion_style": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Development

### Running the Server
```bash
uvicorn backend.src.main:app --reload
```

### API Documentation (Interactive)
When the server is running, visit:
```
http://localhost:8000/docs
```

### Testing
```bash
pytest backend/tests/
```

## Dependencies

- FastAPI
- SQLAlchemy
- Google Generative AI (google-genai >= 1.32.0)
- Python 3.11+
- SQLite (default database)

## Environment Variables

- `GEMINI_API_KEY`: Required for image generation
- `DATABASE_URL`: Optional, defaults to SQLite
