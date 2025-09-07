from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
from datetime import datetime

# Import database setup
from .database import init_database

# Import middleware
from .middleware import setup_middleware

# Import API routers
from .api.projects import router as projects_router
from .api.character import router as character_router
from .api.product import router as product_router
from .api.background import router as background_router
from .api.story import router as story_router
from .api.generate import router as generate_router

app = FastAPI(
    title="Brand Storytelling API",
    description="API for brand storytelling web application",
    version="1.0.0"
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://[::]:3000", "*"],  # Allow frontend server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400  # Cache preflight for 24 hours
)

# Setup custom middleware (logging, error handling)
setup_middleware(app)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

# Include API routers
app.include_router(projects_router, prefix="/api/v1", tags=["projects"])
app.include_router(character_router, prefix="/api/v1", tags=["character"])
app.include_router(product_router, prefix="/api/v1", tags=["product"])
app.include_router(background_router, prefix="/api/v1", tags=["background"])
app.include_router(story_router, prefix="/api/v1", tags=["story"])
app.include_router(generate_router, prefix="/api/v1", tags=["generate"])

@app.get("/")
async def root():
    return {"message": "Brand Storytelling API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
