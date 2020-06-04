"""initial migration

Revision ID: ff5c295fcf77
Revises: 
Create Date: 2020-06-02 01:09:47.985906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff5c295fcf77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.Column('genre', sa.Enum('REGGAE', 'POP', 'TRAP', 'HIP HOP', 'ROCK', 'INDIE', 'HEAVY', 'ELECTRONIC', 'OTHER'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('place', sa.String(length=30), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('date', sa.String(length=30), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('total_available_tickets', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'date', 'city')
    )
    op.create_table('event_artists',
    sa.Column('events_id', sa.Integer(), nullable=True),
    sa.Column('artists_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artists_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['events_id'], ['events.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_artists')
    op.drop_table('events')
    op.drop_table('artists')
    # ### end Alembic commands ###
