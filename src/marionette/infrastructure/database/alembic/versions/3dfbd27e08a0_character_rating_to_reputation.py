"""character:rating to reputation

Revision ID: 3dfbd27e08a0
Revises: 122b9efe6616
Create Date: 2026-11-14 23:44:19.709206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dfbd27e08a0'
down_revision: Union[str, Sequence[str], None] = '122b9efe6616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("characters", "rating", new_column_name="reputation")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("characters", "reputation", new_column_name="rating")
