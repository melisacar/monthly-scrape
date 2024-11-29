"""Create schema

Revision ID: 38149a8d2f1b
Revises: 
Create Date: 2024-10-24 12:30:05.557087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38149a8d2f1b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create schema if it doesn't exist
    op.execute('CREATE SCHEMA IF NOT EXISTS turizm')


def downgrade() -> None:
    # Drop the schema if exists
    op.execute('DROP SCHEMA IF EXISTS turizm CASCADE')