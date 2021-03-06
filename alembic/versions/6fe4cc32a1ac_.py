"""empty message

Revision ID: 6fe4cc32a1ac
Revises: 12e82c01bb43
Create Date: 2021-04-04 22:27:31.753649

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '6fe4cc32a1ac'
down_revision = '12e82c01bb43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ballots', sa.Column('preference', sa.String(), nullable=True))
    op.drop_index('ix_ballots_description', table_name='ballots')
    op.drop_index('ix_ballots_title', table_name='ballots')
    op.create_index(op.f('ix_ballots_preference'), 'ballots', ['preference'], unique=False)
    op.drop_column('ballots', 'description')
    op.drop_column('ballots', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ballots', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('ballots', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_ballots_preference'), table_name='ballots')
    op.create_index('ix_ballots_title', 'ballots', ['title'], unique=False)
    op.create_index('ix_ballots_description', 'ballots', ['description'], unique=False)
    op.drop_column('ballots', 'preference')
    # ### end Alembic commands ###
