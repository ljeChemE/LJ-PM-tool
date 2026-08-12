"""add task and project status fields

Revision ID: 38881e7631a1
Revises: 5dd55bd6b1ee
Create Date: 2026-08-12 09:13:10.897606

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "38881e7631a1"
down_revision: Union[str, None] = "5dd55bd6b1ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Projects: every existing project starts "in_progress", then two
    # already-finished ones (per current real-world state) move to
    # "completed" — a one-time data correction, not a general rule.
    op.add_column("projects", sa.Column("status", sa.String(length=20), nullable=True))
    op.execute("UPDATE projects SET status = 'in_progress'")
    op.alter_column("projects", "status", nullable=False)
    op.create_check_constraint(
        "ck_projects_status", "projects", "status IN ('in_progress', 'completed')"
    )
    op.execute("UPDATE projects SET status = 'completed' WHERE name IN ('BI', 'ECMC')")

    # Tasks: replace the boolean `done` with a 3-stage status, backfilling
    # from the old column before it's dropped (order matters here).
    op.add_column("tasks", sa.Column("status", sa.String(length=20), nullable=True))
    op.execute("UPDATE tasks SET status = CASE WHEN done THEN 'done' ELSE 'todo' END")
    op.alter_column("tasks", "status", nullable=False)
    op.create_check_constraint(
        "ck_tasks_status", "tasks", "status IN ('todo', 'in_progress', 'done')"
    )
    op.drop_column("tasks", "done")


def downgrade() -> None:
    op.add_column("tasks", sa.Column("done", sa.Boolean(), nullable=True))
    op.execute("UPDATE tasks SET done = (status = 'done')")
    op.alter_column("tasks", "done", nullable=False)
    op.drop_constraint("ck_tasks_status", "tasks", type_="check")
    op.drop_column("tasks", "status")

    op.drop_constraint("ck_projects_status", "projects", type_="check")
    op.drop_column("projects", "status")
