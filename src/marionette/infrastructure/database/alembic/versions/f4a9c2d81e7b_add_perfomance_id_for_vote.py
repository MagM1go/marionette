"""votes: perfomance_id column with one-vote-per-publication constraint

Revision ID: f4a9c2d81e7b
Revises: a1c4f7d90b2e
Create Date: 2026-11-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4a9c2d81e7b"
down_revision: Union[str, Sequence[str], None] = "a1c4f7d90b2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("votes", sa.Column("perfomance_id", sa.BigInteger(), nullable=True))
    # NULL (голоса из `/vote`) PostgreSQL считает различными, поэтому
    # ограничение бьёт только по парам (voted_by, perfomance_id).
    op.create_unique_constraint("uq_votes_voted_by_perfomance_id", "votes", ["voted_by", "perfomance_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_votes_voted_by_perfomance_id", "votes", type_="unique")
    op.drop_column("votes", "perfomance_id")
