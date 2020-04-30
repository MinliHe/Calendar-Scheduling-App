"""empty message

Revision ID: 3824f9fc6666
Revises: 3f2859bc374f
Create Date: 2020-04-28 04:05:14.476407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3824f9fc6666'
down_revision = '3f2859bc374f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email_confirmation', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email_confirmation')
    # ### end Alembic commands ###