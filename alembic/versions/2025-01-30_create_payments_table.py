"""Create payments table

Revision ID: af5f0eccc5a0
Revises: d5484eec54a6
Create Date: 2025-01-30 18:28:45.885238

"""

from typing import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'af5f0eccc5a0'
down_revision: str | None = 'd5484eec54a6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE payments (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            payment_data JSONB NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)


def downgrade() -> None:
    op.execute('DROP TABLE payments;')
