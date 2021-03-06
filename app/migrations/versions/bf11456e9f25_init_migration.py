"""init migration

Revision ID: bf11456e9f25
Revises: None
Create Date: 2016-07-10 23:14:48.983000

"""

# revision identifiers, used by Alembic.
revision = 'bf11456e9f25'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('checkMsgs', 'code',
               existing_type=mysql.VARCHAR(length=32),
               nullable=True)
    op.alter_column('checkMsgs', 'phone',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('checkMsgs', 'timestamp',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_index('phone_unique', table_name='checkMsgs')
    op.add_column('users', sa.Column('homeimgurl', sa.String(length=256), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'homeimgurl')
    op.create_index('phone_unique', 'checkMsgs', ['phone'], unique=True)
    op.alter_column('checkMsgs', 'timestamp',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('checkMsgs', 'phone',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('checkMsgs', 'code',
               existing_type=mysql.VARCHAR(length=32),
               nullable=False)
    ### end Alembic commands ###
