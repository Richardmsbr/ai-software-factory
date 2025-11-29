"""
Crew Orchestration
Manages the coordination of multiple AI agents for project execution.
"""
from typing import Any, Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import structlog

from crewai import Crew, Process

from agents.base import BaseAgent
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

logger = structlog.get_logger(__name__)


class ProjectPhase(str, Enum):
    """Project development phases."""
    PLANNING = "planning"
    ARCHITECTURE = "architecture"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"


@dataclass
class CrewResult:
    """Result from crew execution."""
    phase: ProjectPhase
    status: str
    outputs: Dict[str, Any]
    errors: List[str]


class ProjectCrew:
    """
    Orchestrates multiple AI agents to execute a software development project.
    Manages the workflow through different project phases.
    """

    def __init__(self, project_context: Dict[str, Any]):
        """
        Initialize the project crew.

        Args:
            project_context: Project information and requirements
        """
        self.context = project_context
        self.results: List[CrewResult] = []

        # Initialize all agents
        self.agents = {
            "architect": ArchitectAgent(),
            "backend": BackendDeveloperAgent(),
            "frontend": FrontendDeveloperAgent(),
            "database": DatabaseEngineerAgent(),
            "devops": DevOpsEngineerAgent(),
            "qa": QAEngineerAgent(),
            "security": SecurityAnalystAgent(),
            "writer": TechnicalWriterAgent(),
        }

        logger.info(
            "crew_initialized",
            project=project_context.get("project_name"),
            agent_count=len(self.agents)
        )

    def execute_phase(self, phase: ProjectPhase) -> CrewResult:
        """
        Execute a specific project phase.

        Args:
            phase: The phase to execute

        Returns:
            CrewResult with phase outputs
        """
        logger.info("executing_phase", phase=phase.value)

        phase_agents = self._get_phase_agents(phase)
        all_tasks = []

        for agent in phase_agents:
            tasks = agent.get_tasks(self.context)
            all_tasks.extend(tasks)

        if not all_tasks:
            return CrewResult(
                phase=phase,
                status="skipped",
                outputs={},
                errors=["No tasks defined for this phase"]
            )

        crew = Crew(
            agents=[a.agent for a in phase_agents],
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()

            crew_result = CrewResult(
                phase=phase,
                status="completed",
                outputs={"result": result},
                errors=[]
            )

            # Update context with phase outputs
            self._update_context(phase, result)

        except Exception as e:
            logger.error("phase_failed", phase=phase.value, error=str(e))
            crew_result = CrewResult(
                phase=phase,
                status="failed",
                outputs={},
                errors=[str(e)]
            )

        self.results.append(crew_result)
        return crew_result

    def execute_full_pipeline(self) -> List[CrewResult]:
        """
        Execute the complete development pipeline.

        Returns:
            List of results from each phase
        """
        phases = [
            ProjectPhase.PLANNING,
            ProjectPhase.ARCHITECTURE,
            ProjectPhase.DEVELOPMENT,
            ProjectPhase.TESTING,
            ProjectPhase.DEPLOYMENT,
            ProjectPhase.DOCUMENTATION,
        ]

        for phase in phases:
            result = self.execute_phase(phase)

            if result.status == "failed":
                logger.error(
                    "pipeline_stopped",
                    failed_phase=phase.value,
                    errors=result.errors
                )
                break

        return self.results

    def _get_phase_agents(self, phase: ProjectPhase) -> List[BaseAgent]:
        """Get agents responsible for a specific phase."""
        phase_mapping = {
            ProjectPhase.PLANNING: ["architect"],
            ProjectPhase.ARCHITECTURE: ["architect", "database", "security"],
            ProjectPhase.DEVELOPMENT: ["backend", "frontend", "database"],
            ProjectPhase.TESTING: ["qa", "security"],
            ProjectPhase.DEPLOYMENT: ["devops"],
            ProjectPhase.DOCUMENTATION: ["writer"],
        }

        agent_keys = phase_mapping.get(phase, [])
        return [self.agents[key] for key in agent_keys]

    def _update_context(self, phase: ProjectPhase, result: Any) -> None:
        """Update project context with phase outputs."""
        if phase == ProjectPhase.ARCHITECTURE:
            self.context["architecture"] = result
        elif phase == ProjectPhase.PLANNING:
            self.context["api_spec"] = result


class AgentFactory:
    """
    Factory for creating individual agents or specialized crews.
    """

    @staticmethod
    def create_agent(role: str) -> Optional[BaseAgent]:
        """
        Create a single agent by role.

        Args:
            role: Agent role identifier

        Returns:
            Configured agent instance
        """
        agent_map = {
            "architect": ArchitectAgent,
            "backend": BackendDeveloperAgent,
            "frontend": FrontendDeveloperAgent,
            "database": DatabaseEngineerAgent,
            "devops": DevOpsEngineerAgent,
            "qa": QAEngineerAgent,
            "security": SecurityAnalystAgent,
            "writer": TechnicalWriterAgent,
        }

        agent_class = agent_map.get(role.lower())
        if agent_class:
            return agent_class()
        return None

    @staticmethod
    def create_development_crew(context: Dict[str, Any]) -> Crew:
        """Create a crew focused on development tasks."""
        agents = [
            ArchitectAgent(),
            BackendDeveloperAgent(),
            FrontendDeveloperAgent(),
            DatabaseEngineerAgent(),
        ]

        all_tasks = []
        for agent in agents:
            all_tasks.extend(agent.get_tasks(context))

        return Crew(
            agents=[a.agent for a in agents],
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True
        )

    @staticmethod
    def create_review_crew(context: Dict[str, Any]) -> Crew:
        """Create a crew focused on review and quality tasks."""
        agents = [
            QAEngineerAgent(),
            SecurityAnalystAgent(),
        ]

        all_tasks = []
        for agent in agents:
            all_tasks.extend(agent.get_tasks(context))

        return Crew(
            agents=[a.agent for a in agents],
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True
        )
