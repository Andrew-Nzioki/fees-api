"""Initial migration.

Revision ID: 7b0781aa1263
Revises: 
Create Date: 2023-08-09 10:41:15.472693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b0781aa1263'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('group', sa.String(), nullable=True),
    sa.Column('is_client', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('case',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('record', sa.Integer(), nullable=True),
    sa.Column('file_reference', sa.String(), nullable=True),
    sa.Column('clients_reference', sa.String(), nullable=True),
    sa.Column('case_no_or_parties', sa.String(), nullable=True),
    sa.Column('deposit_fees', sa.Integer(), nullable=True),
    sa.Column('final_fees', sa.Integer(), nullable=True),
    sa.Column('deposit_pay', sa.Integer(), nullable=True),
    sa.Column('final_pay', sa.Integer(), nullable=True),
    sa.Column('outstanding', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deposit', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fees')
    op.drop_table('document')
    op.drop_table('case')
    op.drop_table('user')
    # ### end Alembic commands ###
