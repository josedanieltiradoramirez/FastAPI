"""Create_phone_number_for_user column

Revision ID: e9e84dca53fd
Revises: 960843556489
Create Date: 2026-04-20 07:31:54.616090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9e84dca53fd'
down_revision: Union[str, Sequence[str], None] = '960843556489'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(length=32), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
