"""
Database Models
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from database.session import Base


class ProjectStatus(str, enum.Enum):
    """Project status enum"""
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AgentStatus(str, enum.Enum):
    """Agent status enum"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    
    # Requirements
    requirements = Column(JSON)
    user_stories = Column(JSON)
    
    # Architecture
    tech_stack = Column(JSON)
    architecture = Column(JSON)
    
    # Timeline
    estimated_completion = Column(DateTime)
    actual_completion = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="project", cascade="all, delete-orphan")


class Agent(Base):
    """Agent model"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)
    
    # Configuration
    personality = Column(Text)
    skills = Column(JSON)
    tools = Column(JSON)
    
    # Status
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE)
    current_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # Statistics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = relationship("Task", back_populates="assigned_agent", foreign_keys="Task.assigned_to")


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Assignment
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(String(100), ForeignKey("agents.agent_id"))
    
    # Status
    status = Column(String(50), default="pending")
    priority = Column(String(20), default="normal")
    
    # Dependencies
    depends_on = Column(JSON)  # List of task IDs
    
    # Results
    result = Column(JSON)
    error = Column(Text, nullable=True)
    
    # Timeline
    estimated_hours = Column(Integer)
    actual_hours = Column(Integer, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assigned_agent = relationship("Agent", back_populates="tasks", foreign_keys=[assigned_to])


class Message(Base):
    """Message model for agent communication"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Communication
    from_agent = Column(String(100), nullable=False)
    to_agent = Column(String(100), nullable=True)  # Null for broadcast
    channel = Column(String(100), nullable=True)
    
    # Content
    message_type = Column(String(50), default="message")
    subject = Column(String(255))
    content = Column(Text, nullable=False)
    attachments = Column(JSON)
    
    # Context
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # Metadata
    priority = Column(String(20), default="normal")
    requires_response = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="messages")


class APIKey(Base):
    """API Key configuration model"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False, unique=True)
    api_key = Column(String(500), nullable=False)  # Encrypted
    base_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)


class Memory(Base):
    """Memory/Knowledge base model"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), nullable=False, index=True)
    
    # Memory type
    memory_type = Column(String(50), nullable=False)  # short_term, long_term, knowledge
    
    # Content
    content = Column(Text, nullable=False)
    metadata = Column(JSON)
    
    # Context
    project_id = Column(Integer, nullable=True)
    task_id = Column(Integer, nullable=True)
    
    # Vector reference (for ChromaDB)
    vector_id = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    accessed_at = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)
