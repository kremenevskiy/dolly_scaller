"""add referral

Revision ID: bf2ca324465f
Revises: f4410e61107c
Create Date: 2025-02-10 16:52:47.759315

"""

from typing import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bf2ca324465f'
down_revision: str | None = 'f4410e61107c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    """Добавление колонки referral_id и индекса"""
    op.execute("""
        ALTER TABLE users ADD COLUMN referral_id VARCHAR(255) NULL;
    """)
    op.execute("""
        CREATE INDEX idx_users_referral_id ON users (referral_id);
    """)

    # Создаём таблицу referral_log
    op.execute("""
        CREATE TABLE referral_log (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            referral_id VARCHAR(255) NOT NULL,
            subscription_id INT NOT NULL,
            bonus_generations INT NOT NULL DEFAULT 0,
            refer_at TIMESTAMP DEFAULT now()
        );
    """)


def downgrade():
    # Удаляем таблицу referral_log
    op.execute("""
        DROP TABLE IF EXISTS referral_log;
    """)

    """Откат: удаление колонки referral_id и индекса"""
    op.execute("""
        DROP INDEX IF EXISTS idx_users_referral_id;
    """)
    op.execute("""
        ALTER TABLE users DROP COLUMN referral_id;
    """)
