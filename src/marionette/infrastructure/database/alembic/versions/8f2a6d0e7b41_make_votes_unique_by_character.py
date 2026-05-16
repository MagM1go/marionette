"""Make votes unique by character

Revision ID: 8f2a6d0e7b41
Revises: f9db6ca107fe
Create Date: 2026-05-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8f2a6d0e7b41"
down_revision: Union[str, Sequence[str], None] = "f9db6ca107fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        DELETE FROM votes
        WHERE ctid IN (
            SELECT ctid
            FROM (
                SELECT
                    ctid,
                    row_number() OVER (
                        PARTITION BY character_id
                        ORDER BY voted_at DESC, ctid DESC
                    ) AS row_number
                FROM votes
            ) AS ranked_votes
            WHERE ranked_votes.row_number > 1
        )
        """
    )
    op.drop_constraint("votes_pkey", "votes", type_="primary")
    op.create_primary_key("votes_pkey", "votes", ["character_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("votes_pkey", "votes", type_="primary")
    op.create_primary_key("votes_pkey", "votes", ["character_id", "voted_by"])
