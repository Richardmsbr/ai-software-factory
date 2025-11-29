"""
Base Agent Configuration
Provides foundational classes and utilities for all AI agents.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import structlog

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from core.config import settings

logger = structlog.get_logger(__name__)


class AgentRole(str, Enum):
    """Enumeration of available agent roles."""
    PRODUCT_MANAGER = "product_manager"
    ARCHITECT = "architect"
    TECH_LEAD = "tech_lead"
    BACKEND_DEVELOPER = "backend_developer"
    FRONTEND_DEVELOPER = "frontend_developer"
    DATABASE_ENGINEER = "database_engineer"
    DEVOPS_ENGINEER = "devops_engineer"
    QA_ENGINEER = "qa_engineer"
    SECURITY_ANALYST = "security_analyst"
    TECHNICAL_WRITER = "technical_writer"


@dataclass
class AgentConfig:
    """Configuration for an AI agent."""
    role: AgentRole
    goal: str
    backstory: str
    tools: List[Any] = field(default_factory=list)
    verbose: bool = True
    allow_delegation: bool = False
    max_iterations: int = 10
    memory: bool = True


class LLMProvider:
    """Factory for creating LLM instances based on configuration."""

    @staticmethod
    def create(
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Any:
        """
        Create an LLM instance based on the specified provider.

        Args:
            provider: LLM provider name (openai, anthropic, openrouter)
            model: Model identifier
            temperature: Sampling temperature

        Returns:
            Configured LLM instance
        """
        provider = provider or settings.DEFAULT_LLM_PROVIDER
        model = model or settings.DEFAULT_MODEL

        if provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=settings.OPENAI_API_KEY
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                api_key=settings.ANTHROPIC_API_KEY
            )
        elif provider == "openrouter":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    Provides common functionality and enforces interface contracts.
    """

    def __init__(self, config: AgentConfig):
        """
        Initialize the base agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.llm = LLMProvider.create()
        self._agent: Optional[Agent] = None

        logger.info(
            "agent_initialized",
            role=config.role.value,
            goal=config.goal[:50]
        )

    @property
    def agent(self) -> Agent:
        """Get or create the CrewAI agent instance."""
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent

    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configured parameters."""
        return Agent(
            role=self.config.role.value.replace("_", " ").title(),
            goal=self.config.goal,
            backstory=self.config.backstory,
            tools=self.config.tools,
            llm=self.llm,
            verbose=self.config.verbose,
            allow_delegation=self.config.allow_delegation,
            max_iter=self.config.max_iterations,
            memory=self.config.memory
        )

    @abstractmethod
    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """
        Get the list of tasks this agent can perform.

        Args:
            context: Execution context with project information

        Returns:
            List of Task instances
        """
        pass

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's tasks within a crew.

        Args:
            context: Execution context

        Returns:
            Execution results
        """
        tasks = self.get_tasks(context)

        if not tasks:
            logger.warning("no_tasks_defined", role=self.config.role.value)
            return {"status": "no_tasks", "results": []}

        crew = Crew(
            agents=[self.agent],
            tasks=tasks,
            verbose=self.config.verbose
        )

        logger.info(
            "executing_agent",
            role=self.config.role.value,
            task_count=len(tasks)
        )

        result = crew.kickoff()

        logger.info(
            "agent_completed",
            role=self.config.role.value
        )

        return {
            "status": "completed",
            "results": result
        }
