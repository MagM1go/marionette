"""Add reputation field for vote

Revision ID: e4bad03c1a98
Revises: 177ddb3b25c6
Create Date: 2026-11-14 23:32:19.006945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e4bad03c1a98'
down_revision: Union[str, Sequence[str], None] = '177ddb3b25c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
