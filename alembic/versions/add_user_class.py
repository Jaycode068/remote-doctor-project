from alembic import op
import sqlalchemy as sa


revision = '001_add_user'
down_revision = '001_add_notes_appointment'

def upgrade():
    # Drop the existing tables if it exists
    
    # Drop the foreign key constraint from the 'medical_records' table
    op.drop_constraint('medical_records_ibfk_1', 'medical_records', type_='foreignkey')


    
    op.drop_table('patients')

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('address', sa.String(length=100), nullable=True),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=100), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('specialty', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

