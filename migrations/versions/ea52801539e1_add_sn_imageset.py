"""add sn imageset

Revision ID: ea52801539e1
Revises: 8691e9e46f9e
Create Date: 2018-03-23 16:10:15.359368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea52801539e1'
down_revision = '8691e9e46f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imagesets', sa.Column('sn', sa.String(length=16), nullable=False))
    op.create_unique_constraint(None, 'imagesets', ['sn'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'imagesets', type_='unique')
    op.drop_column('imagesets', 'sn')
    # ### end Alembic commands ###
