from alembic import op
import sqlalchemy as sa


revision = '001_add_notes_appointment'
down_revision = '001_remove_doctor_ratings'

def upgrade():
    op.add_column('appointments', sa.Column('notes', sa.String(length=200), nullable=True))

