"""
Middleware for error handling and logging
"""
import logging
import time
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware for logging HTTP requests and responses"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()

        # Log request
        method = scope["method"]
        path = scope["path"]
        query_string = scope["query_string"].decode()
        client = scope.get("client", ("unknown", 0))

        logger.info(f"Request: {method} {path}{query_string} from {client[0]}:{client[1]}")

        # Process request
        await self.app(scope, receive, send)

        # Log response time
        process_time = time.time() - start_time
        logger.info(".2f")

class ErrorHandlingMiddleware:
    """Middleware for handling and logging errors"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            # Log the error
            logger.error(f"Unhandled error: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # Return error response
            error_response = JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_id": f"ERR_{int(time.time())}"
                }
            )

            await error_response(scope, receive, send)

async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTP exceptions"""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.method} {request.url}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}"
        }
    )

async def validation_exception_handler(request: Request, exc):
    """Custom handler for validation errors"""
    logger.warning(f"Validation error: {str(exc)} - {request.method} {request.url}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": str(exc),
            "error_code": "VALIDATION_ERROR"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Custom handler for general exceptions"""
    logger.error(f"General exception: {str(exc)} - {request.method} {request.url}")
    logger.error(f"Traceback: {traceback.format_exc()}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "error_id": f"ERR_{int(time.time())}",
            "error_code": "INTERNAL_ERROR"
        }
    )

def setup_middleware(app):
    """Setup all middleware for the FastAPI app"""

    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Add error handling middleware
    app.add_middleware(ErrorHandlingMiddleware)

    # Add exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Log startup
    logger.info("Middleware setup complete")
    logger.info("Application started successfully")
