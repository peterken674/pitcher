"""Remove likes.

Revision ID: 4117808904a1
Revises: d5d6d8f11bbd
Create Date: 2021-06-15 18:23:36.478524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4117808904a1'
down_revision = 'd5d6d8f11bbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
