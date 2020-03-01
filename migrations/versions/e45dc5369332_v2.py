"""v2

Revision ID: e45dc5369332
Revises: bef1e189f492
Create Date: 2020-01-26 00:05:15.969052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e45dc5369332'
down_revision = 'bef1e189f492'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('matches', sa.Column('loser_id', sa.Integer(), nullable=False))
    op.add_column('matches', sa.Column('winner_id', sa.Integer(), nullable=False))
    op.drop_constraint('matches_loser_username_fkey', 'matches', type_='foreignkey')
    op.drop_constraint('matches_winner_username_fkey', 'matches', type_='foreignkey')
    op.drop_constraint('matches_season_id_fkey', 'matches', type_='foreignkey')
    op.create_foreign_key(None, 'matches', 'scores', ['season_id'], ['season_id'])
    op.create_foreign_key(None, 'matches', 'scores', ['winner_id'], ['id'])
    op.create_foreign_key(None, 'matches', 'scores', ['loser_id'], ['id'])
    op.drop_column('matches', 'winner_username')
    op.drop_column('matches', 'loser_username')
    op.add_column('scores', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scores', 'id')
    op.add_column('matches', sa.Column('loser_username', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.add_column('matches', sa.Column('winner_username', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'matches', type_='foreignkey')
    op.drop_constraint(None, 'matches', type_='foreignkey')
    op.drop_constraint(None, 'matches', type_='foreignkey')
    op.create_foreign_key('matches_season_id_fkey', 'matches', 'seasons', ['season_id'], ['id'])
    op.create_foreign_key('matches_winner_username_fkey', 'matches', 'users', ['winner_username'], ['username'])
    op.create_foreign_key('matches_loser_username_fkey', 'matches', 'users', ['loser_username'], ['username'])
    op.drop_column('matches', 'winner_id')
    op.drop_column('matches', 'loser_id')
    # ### end Alembic commands ###
