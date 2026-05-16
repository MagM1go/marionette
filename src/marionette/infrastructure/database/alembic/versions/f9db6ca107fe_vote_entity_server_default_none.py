"""Vote entity server_default=None

Revision ID: f9db6ca107fe
Revises: 06acfe8b764f
Create Date: 2026-05-14 14:49:45.146054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f9db6ca107fe"
down_revision: Union[str, Sequence[str], None] = "06acfe8b764f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


agencyroles_enum = postgresql.ENUM(
    "DIRECTOR",
    "MANAGER",
    name="agencyroles",
)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    agencyroles_enum.create(bind, checkfirst=True)

    op.create_table(
        "votes",
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.Column("voted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("voted_by", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("character_id", "voted_by"),
    )

    op.add_column(
        "characters",
        sa.Column(
            "agency_role",
            agencyroles_enum,
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("characters", "agency_role")
    op.drop_table("votes")

    agencyroles_enum.drop(op.get_bind(), checkfirst=True)
