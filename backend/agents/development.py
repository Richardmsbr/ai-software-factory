"""
Development Team Agents
Specialized agents for software development tasks.
"""
from typing import Any, Dict, List

from crewai import Task
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    CodeInterpreterTool,
)

from agents.base import BaseAgent, AgentConfig, AgentRole


class ArchitectAgent(BaseAgent):
    """
    Software Architect Agent
    Responsible for system design, architecture decisions, and technical specifications.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.ARCHITECT,
            goal=(
                "Design scalable, maintainable, and secure software architectures "
                "that meet business requirements while following industry best practices."
            ),
            backstory=(
                "You are a senior software architect with 15+ years of experience "
                "designing enterprise systems. You have deep expertise in microservices, "
                "event-driven architecture, and cloud-native design patterns. You excel "
                "at translating business requirements into technical specifications."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ],
            allow_delegation=True
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate architecture tasks based on project context."""
        project_name = context.get("project_name", "Unknown Project")
        requirements = context.get("requirements", {})

        tasks = [
            Task(
                description=f"""
                Analyze the requirements for {project_name} and create a comprehensive
                system architecture document that includes:

                1. High-level system overview
                2. Component diagram with clear boundaries
                3. Data flow between components
                4. Technology stack recommendations with justifications
                5. Scalability considerations
                6. Security architecture
                7. Integration patterns

                Requirements: {requirements}
                """,
                expected_output=(
                    "A detailed architecture document in markdown format with diagrams "
                    "described in ASCII art or mermaid syntax."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Based on the architecture for {project_name}, create detailed
                API specifications including:

                1. RESTful endpoint definitions
                2. Request/Response schemas
                3. Authentication/Authorization flows
                4. Rate limiting strategy
                5. Error handling patterns
                """,
                expected_output=(
                    "OpenAPI 3.0 specification in YAML format with all endpoints, "
                    "schemas, and security definitions."
                ),
                agent=self.agent
            )
        ]

        return tasks


class BackendDeveloperAgent(BaseAgent):
    """
    Backend Developer Agent
    Responsible for implementing server-side logic, APIs, and database operations.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.BACKEND_DEVELOPER,
            goal=(
                "Implement robust, efficient, and well-tested backend services "
                "following clean code principles and design patterns."
            ),
            backstory=(
                "You are a senior backend developer specializing in Python and "
                "FastAPI. You have extensive experience with PostgreSQL, Redis, "
                "and message queues. You write clean, testable code and always "
                "include comprehensive error handling and logging."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
                CodeInterpreterTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate backend development tasks."""
        project_name = context.get("project_name", "Unknown Project")
        architecture = context.get("architecture", {})
        api_spec = context.get("api_spec", {})

        tasks = [
            Task(
                description=f"""
                Implement the database models for {project_name} based on the
                architecture specification:

                Architecture: {architecture}

                Requirements:
                1. Use SQLAlchemy 2.0 with async support
                2. Include all necessary relationships
                3. Add appropriate indexes
                4. Include created_at, updated_at timestamps
                5. Implement soft delete where appropriate
                """,
                expected_output=(
                    "Complete SQLAlchemy model definitions in Python with "
                    "all relationships, indexes, and constraints."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Implement the REST API endpoints for {project_name} based on
                the API specification:

                API Spec: {api_spec}

                Requirements:
                1. Use FastAPI with async/await
                2. Include Pydantic schemas for validation
                3. Implement proper error handling
                4. Add authentication decorators
                5. Include OpenAPI documentation
                """,
                expected_output=(
                    "Complete FastAPI route implementations with all CRUD "
                    "operations, validation, and documentation."
                ),
                agent=self.agent
            )
        ]

        return tasks


class FrontendDeveloperAgent(BaseAgent):
    """
    Frontend Developer Agent
    Responsible for implementing user interfaces and client-side logic.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.FRONTEND_DEVELOPER,
            goal=(
                "Create responsive, accessible, and performant user interfaces "
                "that provide excellent user experience."
            ),
            backstory=(
                "You are a senior frontend developer with expertise in React, "
                "Next.js, and TypeScript. You follow accessibility guidelines "
                "(WCAG 2.1), write semantic HTML, and optimize for performance. "
                "You use modern CSS with Tailwind and implement responsive designs."
            ),
            tools=[
                FileReadTool(),
                DirectoryReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate frontend development tasks."""
        project_name = context.get("project_name", "Unknown Project")
        design_spec = context.get("design_spec", {})
        api_endpoints = context.get("api_endpoints", [])

        tasks = [
            Task(
                description=f"""
                Create the component architecture for {project_name}:

                Design Specification: {design_spec}

                Requirements:
                1. Define component hierarchy
                2. Plan state management strategy
                3. Design reusable component library
                4. Plan routing structure
                5. Define API integration layer
                """,
                expected_output=(
                    "Component architecture document with hierarchy diagram, "
                    "state management plan, and component specifications."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Implement React components for {project_name} based on the
                component architecture:

                API Endpoints: {api_endpoints}

                Requirements:
                1. Use TypeScript with strict mode
                2. Implement with Next.js 14 app router
                3. Use TanStack Query for data fetching
                4. Style with Tailwind CSS
                5. Include loading and error states
                6. Ensure accessibility compliance
                """,
                expected_output=(
                    "Complete React/TypeScript component implementations with "
                    "all required functionality and styling."
                ),
                agent=self.agent
            )
        ]

        return tasks


class DatabaseEngineerAgent(BaseAgent):
    """
    Database Engineer Agent
    Responsible for database design, optimization, and migrations.
    """

    def __init__(self):
        config = AgentConfig(
            role=AgentRole.DATABASE_ENGINEER,
            goal=(
                "Design and optimize database schemas for performance, "
                "reliability, and data integrity."
            ),
            backstory=(
                "You are a database specialist with deep expertise in PostgreSQL. "
                "You understand query optimization, indexing strategies, and "
                "database normalization. You design for both OLTP and OLAP "
                "workloads and implement proper backup and recovery strategies."
            ),
            tools=[
                FileReadTool(),
            ]
        )
        super().__init__(config)

    def get_tasks(self, context: Dict[str, Any]) -> List[Task]:
        """Generate database engineering tasks."""
        project_name = context.get("project_name", "Unknown Project")
        data_model = context.get("data_model", {})

        tasks = [
            Task(
                description=f"""
                Design the database schema for {project_name}:

                Data Model: {data_model}

                Requirements:
                1. Define all tables with appropriate data types
                2. Establish primary and foreign keys
                3. Design indexes for common queries
                4. Plan partitioning strategy if needed
                5. Consider denormalization for read performance
                6. Include audit columns
                """,
                expected_output=(
                    "Complete database schema in SQL DDL format with all "
                    "tables, indexes, constraints, and documentation."
                ),
                agent=self.agent
            ),
            Task(
                description=f"""
                Create Alembic migrations for {project_name}:

                Requirements:
                1. Initial schema migration
                2. Seed data migration
                3. Index creation migration
                4. Include rollback procedures
                """,
                expected_output=(
                    "Alembic migration files with upgrade and downgrade "
                    "functions for all schema changes."
                ),
                agent=self.agent
            )
        ]

        return tasks
