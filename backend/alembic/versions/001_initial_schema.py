"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), server_default='pending', nullable=False),
        sa.Column('requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('user_stories', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tech_stack', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('architecture', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('estimated_completion', sa.DateTime(), nullable=True),
        sa.Column('actual_completion', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_id', 'projects', ['id'])
    op.create_index('ix_projects_status', 'projects', ['status'])
    op.create_index('ix_projects_created_at', 'projects', ['created_at'])

    # Agents table
    op.create_table(
        'agents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.String(100), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(100), nullable=False),
        sa.Column('personality', sa.Text(), nullable=True),
        sa.Column('skills', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('tools', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(50), server_default='idle', nullable=False),
        sa.Column('current_task_id', sa.Integer(), nullable=True),
        sa.Column('total_tasks', sa.Integer(), server_default='0', nullable=False),
        sa.Column('completed_tasks', sa.Integer(), server_default='0', nullable=False),
        sa.Column('failed_tasks', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('agent_id')
    )
    op.create_index('ix_agents_id', 'agents', ['id'])
    op.create_index('ix_agents_agent_id', 'agents', ['agent_id'])
    op.create_index('ix_agents_status', 'agents', ['status'])

    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('assigned_to', sa.String(100), nullable=True),
        sa.Column('status', sa.String(50), server_default='pending', nullable=False),
        sa.Column('priority', sa.String(20), server_default='normal', nullable=False),
        sa.Column('depends_on', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('result', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('estimated_hours', sa.Integer(), nullable=True),
        sa.Column('actual_hours', sa.Integer(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_to'], ['agents.agent_id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'])
    op.create_index('ix_tasks_project_id', 'tasks', ['project_id'])
    op.create_index('ix_tasks_status', 'tasks', ['status'])

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('from_agent', sa.String(100), nullable=False),
        sa.Column('to_agent', sa.String(100), nullable=True),
        sa.Column('channel', sa.String(100), nullable=True),
        sa.Column('message_type', sa.String(50), server_default='message', nullable=False),
        sa.Column('subject', sa.String(255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('attachments', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('priority', sa.String(20), server_default='normal', nullable=False),
        sa.Column('requires_response', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('read', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_messages_id', 'messages', ['id'])
    op.create_index('ix_messages_project_id', 'messages', ['project_id'])
    op.create_index('ix_messages_created_at', 'messages', ['created_at'])

    # API Keys table
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('api_key', sa.String(500), nullable=False),
        sa.Column('base_url', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('provider')
    )
    op.create_index('ix_api_keys_id', 'api_keys', ['id'])
    op.create_index('ix_api_keys_provider', 'api_keys', ['provider'])

    # Memories table
    op.create_table(
        'memories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agent_id', sa.String(100), nullable=False),
        sa.Column('memory_type', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('task_id', sa.Integer(), nullable=True),
        sa.Column('vector_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('accessed_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('access_count', sa.Integer(), server_default='0', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_memories_id', 'memories', ['id'])
    op.create_index('ix_memories_agent_id', 'memories', ['agent_id'])
    op.create_index('ix_memories_memory_type', 'memories', ['memory_type'])


def downgrade() -> None:
    op.drop_table('memories')
    op.drop_table('api_keys')
    op.drop_table('messages')
    op.drop_table('tasks')
    op.drop_table('agents')
    op.drop_table('projects')
