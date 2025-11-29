"""
Projects API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime

from database.session import get_db
from database.models import Project, ProjectStatus

router = APIRouter()


class ProjectCreate(BaseModel):
    """Project creation schema"""
    name: str
    description: Optional[str] = None
    requirements: Optional[dict] = None
    created_by: str = "user"


class ProjectResponse(BaseModel):
    """Project response schema"""
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    requirements: Optional[dict]
    tech_stack: Optional[dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new project"""
    project = Project(
        name=project_data.name,
        description=project_data.description,
        requirements=project_data.requirements,
        created_by=project_data.created_by,
        status=ProjectStatus.PENDING
    )
    
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    return project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all projects"""
    query = select(Project)
    
    if status:
        query = query.where(Project.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Project.created_at.desc())
    
    result = await db.execute(query)
    projects = result.scalars().all()
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get project by ID"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a project"""
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found"
        )
    
    await db.delete(project)
    await db.commit()
