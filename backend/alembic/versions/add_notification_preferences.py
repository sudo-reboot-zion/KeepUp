"""add_notification_preferences

Revision ID: 002_add_notif_prefs
Revises: 001_add_primary_goal
Create Date: 2026-01-22 04:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_notif_prefs'
down_revision = '001_add_primary_goal'  # Assuming this was the previous one
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('notification_preferences', sa.JSON(), nullable=True, comment="User settings for notification timing, channels, and quiet hours"))


def downgrade() -> None:
    op.drop_column('users', 'notification_preferences')
