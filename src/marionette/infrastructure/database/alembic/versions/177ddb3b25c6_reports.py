"""Reports

Revision ID: 177ddb3b25c6
Revises: 0cb286736bf0
Create Date: 2026-11-09 16:14:17.044694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177ddb3b25c6'
down_revision: Union[str, Sequence[str], None] = '0cb286736bf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("reports", "user_id")
    op.add_column("reports", sa.Column("reported_id", sa.BigInteger(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("reports", "reported_id")
