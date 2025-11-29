"""
AI Agents Module
Provides AI-powered agents for autonomous software development.
"""
from agents.base import (
    BaseAgent,
    AgentConfig,
    AgentRole,
    LLMProvider,
)
from agents.development import (
    ArchitectAgent,
    BackendDeveloperAgent,
    FrontendDeveloperAgent,
    DatabaseEngineerAgent,
)
from agents.operations import (
    DevOpsEngineerAgent,
    QAEngineerAgent,
    SecurityAnalystAgent,
    TechnicalWriterAgent,
)
from agents.crew import (
    ProjectCrew,
    ProjectPhase,
    CrewResult,
    AgentFactory,
)

__all__ = [
    # Base
    "BaseAgent",
    "AgentConfig",
    "AgentRole",
    "LLMProvider",
    # Development Agents
    "ArchitectAgent",
    "BackendDeveloperAgent",
    "FrontendDeveloperAgent",
    "DatabaseEngineerAgent",
    # Operations Agents
    "DevOpsEngineerAgent",
    "QAEngineerAgent",
    "SecurityAnalystAgent",
    "TechnicalWriterAgent",
    # Crew
    "ProjectCrew",
    "ProjectPhase",
    "CrewResult",
    "AgentFactory",
]
