"""init

Revision ID: 294eb670e819
Revises:
Create Date: 2023-07-26 20:14:15.502883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "294eb670e819"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
    )
    op.create_table(
        "performer",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nickname", sa.String(255), nullable=False),
    )
    op.create_table(
        "album",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("cover_url", sa.String(255), nullable=False),
        sa.Column("release_date", sa.DateTime(), nullable=False),
        sa.Column("performer_id", sa.Integer(), sa.ForeignKey("performer.id"), nullable=False),
    )
    op.create_table(
        "user_favorite_performer",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("performer_id", sa.Integer(), sa.ForeignKey("performer.id"), nullable=False),
    )
    op.create_table(
        "user_listened_album",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id"), nullable=False),
    )


def downgrade() -> None:
    pass
