"""add status field for Character

Revision ID: 4deb798e8aa9
Revises: 18d66125e12e
Create Date: 2026-04-23 19:18:14.342850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4deb798e8aa9'
down_revision: Union[str, Sequence[str], None] = '18d66125e12e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


characterstatus_enum = postgresql.ENUM(
    "IS_ACTIVE",
    "ABANDONED",
    "MODERATION",
    name="characterstatus",
)


def upgrade() -> None:
    bind = op.get_bind()
    characterstatus_enum.create(bind, checkfirst=True)

    op.add_column(
        "characters",
        sa.Column(
            "status",
            characterstatus_enum,
            nullable=False
        ),
    )

    op.alter_column("characters", "status", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()
    op.drop_column("characters", "status")
    characterstatus_enum.drop(bind, checkfirst=True)
