"""add collaboration

Revision ID: bf8e9d264277
Revises: 68eac4660f16
Create Date: 2023-07-31 17:44:43.526925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bf8e9d264277"
down_revision = "68eac4660f16"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "collaboration",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id"), nullable=False),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artist.id"), nullable=False),
    )
    op.drop_column("album", "artist_id")


def downgrade() -> None:
    op.add_column(
        "album", sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artist.id"), nullable=False)
    )
    op.drop_table("collaboration")
