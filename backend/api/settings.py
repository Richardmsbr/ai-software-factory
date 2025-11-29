"""
Settings API Endpoints - API Key Management
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
from cryptography.fernet import Fernet
import base64

from database.session import get_db
from database.models import APIKey
from core.config import settings as app_settings

router = APIRouter()

# Simple encryption for API keys (use proper key management in production)
def get_cipher():
    """Get Fernet cipher for encryption"""
    key = base64.urlsafe_b64encode(app_settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
    return Fernet(key)


class APIKeyCreate(BaseModel):
    """API Key creation schema"""
    provider: str
    api_key: str
    base_url: Optional[str] = None
    is_active: bool = True


class APIKeyUpdate(BaseModel):
    """API Key update schema"""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    is_active: Optional[bool] = None


class APIKeyResponse(BaseModel):
    """API Key response schema (masked)"""
    id: int
    provider: str
    api_key_masked: str
    base_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_used: Optional[datetime]
    
    class Config:
        from_attributes = True


def mask_api_key(key: str) -> str:
    """Mask API key for display"""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"


@router.get("/api-keys", response_model=List[APIKeyResponse])
async def list_api_keys(db: AsyncSession = Depends(get_db)):
    """List all configured API keys (masked)"""
    result = await db.execute(select(APIKey))
    api_keys = result.scalars().all()
    
    response = []
    cipher = get_cipher()
    
    for key in api_keys:
        try:
            decrypted = cipher.decrypt(key.api_key.encode()).decode()
            masked = mask_api_key(decrypted)
        except:
            masked = "****"
        
        response.append(APIKeyResponse(
            id=key.id,
            provider=key.provider,
            api_key_masked=masked,
            base_url=key.base_url,
            is_active=key.is_active,
            created_at=key.created_at,
            updated_at=key.updated_at,
            last_used=key.last_used
        ))
    
    return response


@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create or update API key"""
    cipher = get_cipher()
    
    # Check if provider already exists
    result = await db.execute(
        select(APIKey).where(APIKey.provider == key_data.provider)
    )
    existing = result.scalar_one_or_none()
    
    # Encrypt API key
    encrypted = cipher.encrypt(key_data.api_key.encode()).decode()
    
    if existing:
        # Update existing
        existing.api_key = encrypted
        if key_data.base_url:
            existing.base_url = key_data.base_url
        existing.is_active = key_data.is_active
        existing.updated_at = datetime.utcnow()
        api_key = existing
    else:
        # Create new
        api_key = APIKey(
            provider=key_data.provider,
            api_key=encrypted,
            base_url=key_data.base_url,
            is_active=key_data.is_active
        )
        db.add(api_key)
    
    await db.commit()
    await db.refresh(api_key)
    
    return APIKeyResponse(
        id=api_key.id,
        provider=api_key.provider,
        api_key_masked=mask_api_key(key_data.api_key),
        base_url=api_key.base_url,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
        last_used=api_key.last_used
    )


@router.patch("/api-keys/{provider}", response_model=APIKeyResponse)
async def update_api_key(
    provider: str,
    key_data: APIKeyUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update API key"""
    result = await db.execute(
        select(APIKey).where(APIKey.provider == provider)
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key for provider '{provider}' not found"
        )
    
    cipher = get_cipher()
    
    if key_data.api_key:
        api_key.api_key = cipher.encrypt(key_data.api_key.encode()).decode()
    
    if key_data.base_url is not None:
        api_key.base_url = key_data.base_url
    
    if key_data.is_active is not None:
        api_key.is_active = key_data.is_active
    
    api_key.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(api_key)
    
    # Get masked key
    try:
        decrypted = cipher.decrypt(api_key.api_key.encode()).decode()
        masked = mask_api_key(decrypted)
    except:
        masked = "****"
    
    return APIKeyResponse(
        id=api_key.id,
        provider=api_key.provider,
        api_key_masked=masked,
        base_url=api_key.base_url,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
        last_used=api_key.last_used
    )


@router.delete("/api-keys/{provider}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    provider: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete API key"""
    result = await db.execute(
        select(APIKey).where(APIKey.provider == provider)
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API key for provider '{provider}' not found"
        )
    
    await db.delete(api_key)
    await db.commit()


@router.get("/config")
async def get_configuration():
    """Get current system configuration (non-sensitive)"""
    return {
        "app_name": app_settings.APP_NAME,
        "version": app_settings.VERSION,
        "default_llm_provider": app_settings.DEFAULT_LLM_PROVIDER,
        "default_model": app_settings.DEFAULT_MODEL,
        "max_agents": app_settings.MAX_AGENTS,
        "max_concurrent_projects": app_settings.MAX_CONCURRENT_PROJECTS,
        "memory_backend": app_settings.MEMORY_BACKEND,
        "ollama_available": app_settings.OLLAMA_BASE_URL is not None,
    }
