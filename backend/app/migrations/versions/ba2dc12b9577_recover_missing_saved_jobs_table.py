"""Recover missing saved_jobs table

Revision ID: ba2dc12b9577
Revises: 00d565e9ca74
Create Date: 2025-06-10 10:50:55.349515

"""
"""Recover missing saved_jobs table"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers
revision = 'ba2dc12b9577'  # replace with your generated revision
down_revision = '00d565e9ca74'
branch_labels = None
depends_on = None

def upgrade():
    # Check if table exists
    conn = op.get_bind()
    result = conn.execute(
        text("SELECT to_regclass('public.saved_jobs');")
    ).scalar()

    if result is None:
        # Table does not exist — create it
        op.create_table(
            'saved_jobs',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
            sa.Column('search_id', sa.String(), nullable=False),
            sa.Column('job_title', sa.String(), nullable=False),
            sa.Column('employer_name', sa.String(), nullable=False),
            sa.Column('employer_logo', sa.String()),
            sa.Column('employer_website', sa.String()),
            sa.Column('job_location', sa.String()),
            sa.Column('job_is_remote', sa.Boolean(), default=False),
            sa.Column('job_employment_type', sa.String()),
            sa.Column('job_salary', sa.String(), nullable=True),
            sa.Column('job_description', sa.Text(), nullable=True),
            sa.Column('job_apply_link', sa.String(), nullable=False),
            sa.Column('job_posted_at', sa.DateTime(), nullable=False),
            sa.Column('saved_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.UniqueConstraint('user_id', 'search_id', name='uq_user_search'),
        )
        print("✅ Created saved_jobs table.")
    else:
        print("ℹ️  saved_jobs table already exists — skipping.")

def downgrade():
    # Optional: drop the table if needed
    op.drop_table('saved_jobs')
