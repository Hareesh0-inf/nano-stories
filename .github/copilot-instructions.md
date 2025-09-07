# GitHub Copilot Instructions

## Project Overview
This is a web application for brand storytelling using AI image generation. It has a Python FastAPI backend with Gemini API integration and a vanilla JavaScript frontend.

## Tech Stack
- Backend: Python 3.11, FastAPI, SQLAlchemy, google-genai >=1.32.0
- Frontend: Vanilla JavaScript, HTML, CSS
- AI: Gemini API with gemini-2.5-flash-image-preview (Nano Banana)
- Database: SQLite

## Development Guidelines
- Follow TDD: Write tests before implementation
- Use async/await for FastAPI endpoints
- Keep frontend simple with no frameworks
- Use fetch API for HTTP requests
- Handle file uploads with FormData
- Store images as URLs or base64

## Code Style
- Python: PEP 8, type hints
- JavaScript: ES6+, camelCase
- HTML/CSS: Semantic, accessible

## Recent Changes
- Initial setup with FastAPI and Gemini integration
- Basic frontend structure
- Data model for projects and entities
