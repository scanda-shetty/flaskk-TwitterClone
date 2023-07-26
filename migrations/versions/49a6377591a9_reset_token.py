"""reset_token

Revision ID: 49a6377591a9
Revises: 
Create Date: 2023-07-22 00:16:37.579214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49a6377591a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_mgmt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_token', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_mgmt', schema=None) as batch_op:
        batch_op.drop_column('reset_token')

    # ### end Alembic commands ###