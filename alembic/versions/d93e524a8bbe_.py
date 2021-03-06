"""empty message

Revision ID: d93e524a8bbe
Revises: 6fe4cc32a1ac
Create Date: 2021-04-04 22:52:17.759623

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd93e524a8bbe'
down_revision = '6fe4cc32a1ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('election_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['election_id'], ['elections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidates_id'), 'candidates', ['id'], unique=False)
    op.create_index(op.f('ix_candidates_info'), 'candidates', ['info'], unique=False)
    op.add_column('ballots', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ballots', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ballots', type_='foreignkey')
    op.drop_column('ballots', 'owner_id')
    op.drop_index(op.f('ix_candidates_info'), table_name='candidates')
    op.drop_index(op.f('ix_candidates_id'), table_name='candidates')
    op.drop_table('candidates')
    # ### end Alembic commands ###
