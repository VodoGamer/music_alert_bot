"""rename performer to artist

Revision ID: 68eac4660f16
Revises: 294eb670e819
Create Date: 2023-07-29 18:02:16.797409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "68eac4660f16"
down_revision = "294eb670e819"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("performer", "artist")
    op.alter_column("album", "performer_id", new_column_name="artist_id")
    op.rename_table("user_favorite_performer", "user_favorite_artist")
    op.alter_column("user_favorite_artist", "performer_id", new_column_name="artist_id")


def downgrade() -> None:
    op.rename_table("artist", "performer")
    op.alter_column("album", "artist_id", new_column_name="performer_id")
    op.rename_table("user_favorite_artist", "user_favorite_performer")
    op.alter_column("user_favorite_artist", "artist_id", new_column_name="performer_id")
