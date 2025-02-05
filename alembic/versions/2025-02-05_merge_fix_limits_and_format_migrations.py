"""Merge fix-limits and format migrations

Revision ID: f4410e61107c
Revises: c51c3e6e3adf, 6f7a38a03aab
Create Date: 2025-02-05 11:53:34.217936

"""

from typing import Sequence

# revision identifiers, used by Alembic.
revision: str = 'f4410e61107c'
down_revision: str | None = ('c51c3e6e3adf', '6f7a38a03aab')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
