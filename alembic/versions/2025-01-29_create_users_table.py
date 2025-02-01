"""Create users table

Revision ID: 56944a7590ee
Revises:
Create Date: 2025-01-29 16:38:46.057063

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '56944a7590ee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE users (
            user_id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255),
            user_first_name VARCHAR(255),
            user_last_name VARCHAR(255),
            tg_premium BOOLEAN,
            user_type VARCHAR(255),
            models_max INTEGER,
            date_joined TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS users;')
