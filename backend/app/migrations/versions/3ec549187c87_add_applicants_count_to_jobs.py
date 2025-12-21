"""add applicants_count to jobs

Revision ID: 3ec549187c87
Revises: ba2dc12b9577
Create Date: 2025-12-20 16:18:31.406878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ec549187c87'
down_revision: Union[str, None] = 'ba2dc12b9577'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS applicants_count TEXT;")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE jobs DROP COLUMN IF EXISTS applicants_count;")
    # ### end Alembic commands ###
