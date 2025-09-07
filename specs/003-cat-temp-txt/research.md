# ## Gemini API
- Decision: Use google-genai >=1.32.0
- Rationale: Latest stable version for Python with full Gemini API support
- Alternatives considered: Older versions

## Nano-banana Model
- Decision: Use gemini-2.5-flash-image-preview (Nano Banana model)
- Rationale: Specified in requirements, latest image generation model
- Alternatives considered: Other Gemini modelsFindings

## FastAPI
- Decision: Use FastAPI 0.104.1
- Rationale: Latest version with async support and automatic OpenAPI generation
- Alternatives considered: Flask (less async support), Django (heavier)

## Vanilla JS
- Decision: Use fetch API and FormData for file uploads
- Rationale: Native browser APIs, no external dependencies needed
- Alternatives considered: Axios (adds dependency), jQuery (outdated)
