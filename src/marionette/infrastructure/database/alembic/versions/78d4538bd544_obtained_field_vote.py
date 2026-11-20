"""Obtained field Vote

Revision ID: 78d4538bd544
Revises: f4a9c2d81e7b
Create Date: 2026-11-20 14:14:28.686069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '78d4538bd544'
down_revision: Union[str, Sequence[str], None] = 'f4a9c2d81e7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("votes", sa.Column("obtained", sa.Boolean(), server_default=sa.false(), nullable=False))

def downgrade() -> None:
    op.drop_column("votes", "obtained")
