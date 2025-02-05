"""merge_limits_count

Revision ID: 6f7a38a03aab
Revises: 4bf5f870ba86
Create Date: 2025-02-04 21:12:05.506320

"""

from typing import Sequence
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6f7a38a03aab'
down_revision: str | None = '4bf5f870ba86'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('user_subscriptions', sa.Column('generation_photos_left', sa.Integer(), nullable=False, server_default='0'))

    # Заполняем новое поле суммой старых значений
    op.execute("""
        UPDATE user_subscriptions
        SET generation_photos_left = photos_by_prompt_left + photos_by_image_left;
    """)

    # Удаляем старые поля
    op.drop_column('user_subscriptions', 'photos_by_prompt_left')
    op.drop_column('user_subscriptions', 'photos_by_image_left')

    # Добавляем новое поле в subscriptions_details
    op.add_column('subscriptions_details', sa.Column('generation_photos_count', sa.Integer(), nullable=False, server_default='0'))

    # Заполняем новое поле суммой старых значений
    op.execute("""
        UPDATE subscriptions_details
        SET generation_photos_count = photos_by_prompt_count + photos_by_image_count;
    """)

    # Удаляем старые поля
    op.drop_column('subscriptions_details', 'photos_by_prompt_count')
    op.drop_column('subscriptions_details', 'photos_by_image_count')
    pass


def downgrade() -> None:
    op.add_column('user_subscriptions', sa.Column('photos_by_prompt_left', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user_subscriptions', sa.Column('photos_by_image_left', sa.Integer(), nullable=False, server_default='0'))

    # Восстанавливаем данные, разделяя на два поля (делим поровну, при необходимости можно скорректировать логику)
    op.execute("""
        UPDATE user_subscriptions
        SET photos_by_prompt_left = generation_photos_left / 2,
            photos_by_image_left = generation_photos_left / 2;
    """)

    # Удаляем новое поле
    op.drop_column('user_subscriptions', 'generation_photos_left')

    # Добавляем старые поля обратно в subscriptions_details
    op.add_column('subscriptions_details', sa.Column('photos_by_prompt_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('subscriptions_details', sa.Column('photos_by_image_count', sa.Integer(), nullable=False, server_default='0'))

    # Восстанавливаем данные, разделяя на два поля
    op.execute("""
        UPDATE subscriptions_details
        SET photos_by_prompt_count = generation_photos_count / 2,
            photos_by_image_count = generation_photos_count / 2;
    """)

    # Удаляем новое поле
    op.drop_column('subscriptions_details', 'generation_photos_count')
    pass
