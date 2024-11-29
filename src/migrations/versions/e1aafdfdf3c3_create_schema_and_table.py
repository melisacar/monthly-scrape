"""Create turizm schema and updated table

Revision ID: e1aafdfdf3c3
Revises: 38149a8d2f1b
Create Date: 2024-11-28 11:59:24.471104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1aafdfdf3c3'
down_revision: Union[str, None] = '38149a8d2f1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create turizm schema if not exists
    op.execute('CREATE SCHEMA IF NOT EXISTS turizm')

    # Create tum_ucuslar_aylik table
    op.create_table(
        'tum_ucuslar_aylik',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('havalimani', sa.String, nullable=True),
        sa.Column('hat_turu', sa.String, nullable=True),
        sa.Column('num', sa.Float, nullable=True),
        sa.Column('kategori', sa.String, nullable=True),
        sa.Column('tarih', sa.Date, nullable=True),
        sa.Column('erisim_tarihi', sa.Date, nullable=True),
        sa.UniqueConstraint('havalimani', 'hat_turu', 'kategori', 'tarih', name='unique_ucuslar'),
        schema='turizm'
    )


def downgrade() -> None:
    # Drop tum_ucuslar_aylik table
    op.drop_table('tum_ucuslar_aylik', schema='turizm')

    # Drop turizm schema
    op.execute('DROP SCHEMA IF EXISTS turizm CASCADE')
