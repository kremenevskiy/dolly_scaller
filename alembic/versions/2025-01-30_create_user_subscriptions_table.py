"""Create user subscriptions  table

Revision ID: 4bf5f870ba86
Revises: af5f0eccc5a0
Create Date: 2025-01-30 18:29:39.674776

"""

from typing import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4bf5f870ba86'
down_revision: str | None = 'af5f0eccc5a0'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE user_subscriptions (
            id SERIAL PRIMARY KEY,
            subscription_id INT NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            start_date TIMESTAMP WITH TIME ZONE NOT NULL,
            end_date TIMESTAMP WITH TIME ZONE,
            photos_by_prompt_left INT NOT NULL DEFAULT 0,
            photos_by_image_left INT NOT NULL DEFAULT 0,
            status VARCHAR(100) NOT NULL
        );
    """)
    op.execute("""
        CREATE TABLE models (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            gender VARCHAR(100) NOT NULL,
            link_to_adls VARCHAR(255),
            status VARCHAR(100) NOT NULL,
            photo_info VARCHAR(255)
        );
    """)


def downgrade() -> None:
    op.execute('DROP TABLE user_subscriptions;')
    op.execute('DROP TABLE models')
