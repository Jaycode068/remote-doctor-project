from alembic import op
import sqlalchemy as sa


revision = '001_add_username_password'
down_revision = None


# Upgrade function
def upgrade():
    op.add_column('patients', sa.Column('username', sa.String(50), nullable=False))
    op.add_column('patients', sa.Column('password', sa.String(100), nullable=False))

    op.add_column('doctors', sa.Column('username', sa.String(50), nullable=False))
    op.add_column('doctors', sa.Column('password', sa.String(100), nullable=False))


