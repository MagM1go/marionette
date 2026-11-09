"""Reports

Revision ID: 0cb286736bf0
Revises: bcad8f308869
Create Date: 2026-11-09 16:10:40.894262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cb286736bf0'
down_revision: Union[str, Sequence[str], None] = 'bcad8f308869'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("reports",
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issuer_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('reason', sa.String, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reports")
