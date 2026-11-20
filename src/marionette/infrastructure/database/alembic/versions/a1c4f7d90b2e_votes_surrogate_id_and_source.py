"""votes: surrogate id PK and source column

Revision ID: a1c4f7d90b2e
Revises: 3dfbd27e08a0
Create Date: 2026-11-15 08:02:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "a1c4f7d90b2e"
down_revision: Union[str, Sequence[str], None] = "3dfbd27e08a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


votesource_enum = postgresql.ENUM(
    "COMMAND",
    "REVIEW",
    name="votesource",
)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    votesource_enum.create(bind, checkfirst=True)

    op.add_column("votes", sa.Column("id", sa.BigInteger(), nullable=True))
    op.execute(
        """
        UPDATE votes
        SET id = ranked_votes.rn
        FROM (
            SELECT
                ctid,
                row_number() OVER (ORDER BY voted_at, ctid) AS rn
            FROM votes
        ) AS ranked_votes
        WHERE votes.ctid = ranked_votes.ctid
        """
    )
    op.alter_column("votes", "id", existing_type=sa.BigInteger(), nullable=False)
    op.drop_constraint("votes_pkey", "votes", type_="primary")
    op.create_primary_key("votes_pkey", "votes", ["id"])

    op.add_column(
        "votes",
        sa.Column("source", votesource_enum, nullable=False, server_default="COMMAND"),
    )
    op.create_index("ix_votes_character_id", "votes", ["character_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_votes_character_id", table_name="votes")

    op.execute(
        """
        DELETE FROM votes
        WHERE source != 'COMMAND'
           OR id IN (
               SELECT id
               FROM (
                   SELECT
                       id,
                       row_number() OVER (
                           PARTITION BY character_id
                           ORDER BY voted_at DESC, id DESC
                       ) AS row_number
                   FROM votes
                   WHERE source = 'COMMAND'
               ) AS ranked_votes
               WHERE ranked_votes.row_number > 1
           )
        """
    )
    op.drop_column("votes", "source")
    op.drop_constraint("votes_pkey", "votes", type_="primary")
    op.create_primary_key("votes_pkey", "votes", ["character_id"])
    op.drop_column("votes", "id")

    votesource_enum.drop(op.get_bind(), checkfirst=True)
