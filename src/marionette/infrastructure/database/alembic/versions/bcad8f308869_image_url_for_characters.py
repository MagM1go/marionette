"""Image url for characters

Revision ID: bcad8f308869
Revises: 9525a3b0c2de
Create Date: 2026-11-07 16:44:40.673479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcad8f308869'
down_revision: Union[str, Sequence[str], None] = '9525a3b0c2de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("characters", sa.Column("image_url", sa.String(), nullable=True, server_default=None))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("characters", "image_url")
