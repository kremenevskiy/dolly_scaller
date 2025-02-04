"""Formates table

Revision ID: c51c3e6e3adf
Revises: 4bf5f870ba86
Create Date: 2025-02-04 13:37:30.730897

"""

from typing import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c51c3e6e3adf'
down_revision: str | None = '4bf5f870ba86'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE formats (
            id SERIAL PRIMARY KEY,
            format VARCHAR(255) NOT NULL,
            height INT NOT NULL,
            width INT NOT NULL
        );
    """)

    op.execute("""
        CREATE TABLE user_profiles (
            user_id VARCHAR(255) PRIMARY KEY,
            format_id INT NOT NULL
        );
    """)


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS formats;')
    op.execute('DROP TABLE IF EXISTS user_profiles;')
