"""
Agents API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime

from database.session import get_db
from database.models import Agent, AgentStatus

router = APIRouter()


class AgentResponse(BaseModel):
    """Agent response schema"""
    id: int
    agent_id: str
    name: str
    role: str
    status: AgentStatus
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[AgentStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all agents"""
    query = select(Agent)
    
    if status:
        query = query.where(Agent.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Agent.name)
    
    result = await db.execute(query)
    agents = result.scalars().all()
    
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get agent by ID"""
    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    return agent


@router.get("/{agent_id}/stats")
async def get_agent_stats(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get agent statistics"""
    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    success_rate = 0
    if agent.total_tasks > 0:
        success_rate = (agent.completed_tasks / agent.total_tasks) * 100
    
    return {
        "agent_id": agent.agent_id,
        "name": agent.name,
        "role": agent.role,
        "status": agent.status,
        "statistics": {
            "total_tasks": agent.total_tasks,
            "completed_tasks": agent.completed_tasks,
            "failed_tasks": agent.failed_tasks,
            "success_rate": round(success_rate, 2)
        }
    }
