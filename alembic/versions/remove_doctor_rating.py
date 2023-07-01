from alembic import op
import sqlalchemy as sa


revision = '001_remove_doctor_ratings'
down_revision = '001_add_username_password'


def upgrade():
    op.drop_column('doctors', 'rating')


def downgrade():
    op.add_column('doctors', sa.Column('rating', sa.Float))

