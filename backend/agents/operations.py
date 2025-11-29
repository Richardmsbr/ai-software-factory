"""
Operations Team Agents
Specialized agents for DevOps, QA, and security tasks.
"""
from typing import Any, Dict, List

from crewai import Task
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
)

from agents.base import BaseAgent, AgentConfig, AgentRole


class DevOpsEngineerAgent(BaseAgent):
    """
    DevOps Engineer Agent
    Responsible for CI/CD, infrastructure, and deployment automation.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.DEVOPS_ENGINEER,
            goal=(
                "Design and implement robust CI/CD pipelines, infrastructure "
                "as code, and deployment automation for reliable software delivery."
            ),
            backstory=(
                "You are a senior DevOps engineer with expertise in Docker, "
                "Kubernetes, Terraform, and GitHub Actions. You implement "
                "GitOps workflows, design for high availability, and ensure "
                "zero-downtime deployments. You follow security best practices "
                "and implement comprehensive monitoring."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate DevOps tasks."""
        project_name = context.get("project_name", "Unknown Project")
        architecture = context.get("architecture", {})

        tasks = [
            Task(
                description=f"""
                Create Docker configuration for {project_name}:

                Architecture: {architecture}

                Requirements:
                1. Multi-stage Dockerfile for each service
                2. Docker Compose for local development
                3. Optimize image sizes
                4. Include health checks
                5. Configure proper networking
                6. Set up volume mounts for persistence
                """,
                expected_output=(
                    "Complete Dockerfile and docker-compose.yml with all "
                    "services, networks, and volumes configured."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Create CI/CD pipeline for {project_name}:

                Requirements:
                1. GitHub Actions workflow
                2. Build and test stages
                3. Security scanning (SAST/DAST)
                4. Container image building and pushing
                5. Deployment to staging and production
                6. Rollback procedures
                """,
                expected_output=(
                    "Complete GitHub Actions workflow files with all stages, "
                    "secrets management, and environment configurations."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Create infrastructure as code for {project_name}:

                Requirements:
                1. Terraform modules for cloud resources
                2. Kubernetes manifests or Helm charts
                3. Network security groups
                4. Load balancer configuration
                5. Auto-scaling policies
                6. Monitoring and alerting setup
                """,
                expected_output=(
                    "Complete Terraform configurations and Kubernetes manifests "
                    "for production deployment."
                ),
                agent=self.agent
            )
        ]

        return tasks


class QAEngineerAgent(BaseAgent):
    """
    QA Engineer Agent
    Responsible for test planning, automation, and quality assurance.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.QA_ENGINEER,
            goal=(
                "Ensure software quality through comprehensive testing strategies, "
                "automated test suites, and continuous quality monitoring."
            ),
            backstory=(
                "You are a senior QA engineer with expertise in test automation. "
                "You design test strategies covering unit, integration, e2e, and "
                "performance testing. You use pytest for backend, Jest/Playwright "
                "for frontend, and implement quality gates in CI/CD pipelines."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate QA tasks."""
        project_name = context.get("project_name", "Unknown Project")
        requirements = context.get("requirements", {})

        tasks = [
            Task(
                description=f"""
                Create test strategy for {project_name}:

                Requirements: {requirements}

                Include:
                1. Test pyramid structure
                2. Coverage targets for each layer
                3. Test environment requirements
                4. Data management strategy
                5. Performance testing approach
                6. Security testing scope
                """,
                expected_output=(
                    "Comprehensive test strategy document with detailed "
                    "approach for each testing layer."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Implement backend test suite for {project_name}:

                Requirements:
                1. Unit tests with pytest
                2. Integration tests for API endpoints
                3. Database tests with test fixtures
                4. Mock external dependencies
                5. Achieve 80%+ code coverage
                6. Include performance benchmarks
                """,
                expected_output=(
                    "Complete pytest test suite with fixtures, mocks, "
                    "and configuration for CI integration."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Implement frontend test suite for {project_name}:

                Requirements:
                1. Component tests with Jest/React Testing Library
                2. E2E tests with Playwright
                3. Visual regression tests
                4. Accessibility tests
                5. Performance budgets
                """,
                expected_output=(
                    "Complete frontend test suite with component tests, "
                    "E2E scenarios, and CI configuration."
                ),
                agent=self.agent
            )
        ]

        return tasks


class SecurityAnalystAgent(BaseAgent):
    """
    Security Analyst Agent
    Responsible for security assessments, threat modeling, and compliance.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.SECURITY_ANALYST,
            goal=(
                "Identify and mitigate security risks through threat modeling, "
                "security testing, and implementation of security controls."
            ),
            backstory=(
                "You are a senior security analyst with expertise in application "
                "security. You conduct threat modeling using STRIDE, perform "
                "security code reviews, and ensure compliance with OWASP guidelines. "
                "You implement security controls for authentication, authorization, "
                "and data protection."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate security tasks."""
        project_name = context.get("project_name", "Unknown Project")
        architecture = context.get("architecture", {})

        tasks = [
            Task(
                description=f"""
                Perform threat modeling for {project_name}:

                Architecture: {architecture}

                Requirements:
                1. Identify trust boundaries
                2. Apply STRIDE methodology
                3. Document threat scenarios
                4. Prioritize by risk level
                5. Recommend mitigations
                """,
                expected_output=(
                    "Threat model document with identified threats, "
                    "risk ratings, and mitigation strategies."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Define security requirements for {project_name}:

                Requirements:
                1. Authentication mechanisms (OAuth2/OIDC)
                2. Authorization model (RBAC/ABAC)
                3. Data encryption (at rest and in transit)
                4. Input validation rules
                5. Audit logging requirements
                6. Compliance controls (GDPR, SOC2)
                """,
                expected_output=(
                    "Security requirements specification with implementation "
                    "guidance for each control."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Create security testing plan for {project_name}:

                Requirements:
                1. SAST tool configuration
                2. DAST scanning scope
                3. Dependency vulnerability scanning
                4. Penetration testing scope
                5. Security regression tests
                """,
                expected_output=(
                    "Security testing plan with tool configurations, "
                    "test cases, and CI integration."
                ),
                agent=self.agent
            )
        ]

        return tasks


class TechnicalWriterAgent(BaseAgent):
    """
    Technical Writer Agent
    Responsible for documentation, API references, and user guides.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.TECHNICAL_WRITER,
            goal=(
                "Create clear, comprehensive, and maintainable documentation "
                "that enables users and developers to effectively use the system."
            ),
            backstory=(
                "You are a senior technical writer with experience documenting "
                "complex software systems. You create API documentation, user "
                "guides, and developer documentation. You follow docs-as-code "
                "practices and ensure documentation stays in sync with code."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate documentation tasks."""
        project_name = context.get("project_name", "Unknown Project")
        api_spec = context.get("api_spec", {})

        tasks = [
            Task(
                description=f"""
                Create API documentation for {project_name}:

                API Specification: {api_spec}

                Requirements:
                1. Getting started guide
                2. Authentication guide
                3. Endpoint reference with examples
                4. Error code reference
                5. Rate limiting documentation
                6. SDK examples (curl, Python, JavaScript)
                """,
                expected_output=(
                    "Complete API documentation in markdown format with "
                    "examples, diagrams, and code samples."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Create developer documentation for {project_name}:

                Requirements:
                1. Local development setup
                2. Architecture overview
                3. Code contribution guidelines
                4. Testing guide
                5. Deployment guide
                6. Troubleshooting guide
                """,
                expected_output=(
                    "Complete developer documentation enabling new "
                    "developers to contribute to the project."
                ),
                agent=self.agent
            )
        ]

        return tasks
