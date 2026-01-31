"""Add primary_goal tracking

Revision ID: add_primary_goal
Revises: 
Create Date: 2026-01-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_primary_goal'
down_revision = None  # Update this with your latest migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add primary_goal fields to users table
    op.add_column('users', sa.Column('primary_goal', sa.String(length=50), nullable=True, comment="User's primary health focus: fitness|sleep|stress|wellness"))
    op.add_column('users', sa.Column('goal_details', sa.JSON(), nullable=True, comment="Rich context about user's specific goal"))
    op.add_column('users', sa.Column('goal_set_at', sa.DateTime(timezone=True), nullable=True, comment="When user set their primary goal"))
    
    # Add primary_goal fields to resolutions table
    op.add_column('resolutions', sa.Column('primary_goal', sa.String(length=50), nullable=True, comment="User's primary health focus: fitness|sleep|stress|wellness"))
    op.add_column('resolutions', sa.Column('supporting_goals', sa.JSON(), nullable=True, comment="Secondary goals that support primary goal"))
    op.add_column('resolutions', sa.Column('goal_focus_percentage', sa.JSON(), nullable=True, comment="How focus is split: {primary: 70, supporting: 30}"))


def downgrade() -> None:
    # Remove columns from resolutions table
    op.drop_column('resolutions', 'goal_focus_percentage')
    op.drop_column('resolutions', 'supporting_goals')
    op.drop_column('resolutions', 'primary_goal')
    
    # Remove columns from users table
    op.drop_column('users', 'goal_set_at')
    op.drop_column('users', 'goal_details')
    op.drop_column('users', 'primary_goal')
