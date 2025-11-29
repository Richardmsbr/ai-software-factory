"""
Health Check Endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as redis

from database.session import get_db
from core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "AI Software Factory",
        "version": settings.VERSION
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with all services"""
    health_status = {
        "status": "healthy",
        "services": {}
    }
    
    # Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Ollama (if configured)
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            if response.status_code == 200:
                health_status["services"]["ollama"] = "healthy"
            else:
                health_status["services"]["ollama"] = "unhealthy"
    except Exception as e:
        health_status["services"]["ollama"] = f"unavailable: {str(e)}"
    
    return health_status
