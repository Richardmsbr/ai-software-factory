"""
AI Software Factory - Main Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api import health, projects, agents, settings
from core.config import settings as app_settings
from database.session import init_db
from utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AI Software Factory...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Software Factory...")


app = FastAPI(
    title="AI Software Factory",
    description="Enterprise-grade autonomous software development factory",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if app_settings.DEBUG else "An error occurred"
        }
    )


# API Routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Software Factory",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=app_settings.DEBUG,
        log_level="info"
    )
