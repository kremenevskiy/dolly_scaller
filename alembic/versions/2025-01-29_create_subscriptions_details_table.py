"""Create subscriptions_details table

Revision ID: d5484eec54a6
Revises: 56944a7590ee
Create Date: 2025-01-29 21:52:04.056853

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d5484eec54a6"
down_revision: Union[str, None] = "56944a7590ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE subscriptions_details (
            id SERIAL PRIMARY KEY,
            subscription_name VARCHAR(255) NOT NULL,
            subscription_type VARCHAR(100) NOT NULL,
            cost_rubles INT NOT NULL,
            cost_stars INT NOT NULL,
            duration INT,
            start_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMP WITH TIME ZONE,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            models_count INT NOT NULL DEFAULT 0,
            photos_by_prompt_count INT NOT NULL DEFAULT 0,
            photos_by_image_count INT NOT NULL DEFAULT 0
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE subscriptions_details;")
