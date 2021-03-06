"""empty message

Revision ID: 88676c2fdaa1
Revises: 4f5dbe9502f5
Create Date: 2021-04-05 14:58:43.918632

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '88676c2fdaa1'
down_revision = '4f5dbe9502f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('elections', sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('elections', 'created_date')
    # ### end Alembic commands ###
