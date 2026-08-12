"""seed fixed hashtag projects

Revision ID: 5dd55bd6b1ee
Revises: 357a5d552d16
Create Date: 2026-08-11 23:33:13.322886

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5dd55bd6b1ee"
down_revision: Union[str, None] = "357a5d552d16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Fixed hashtag categories — not user-creatable; the frontend's "Add
# project" form was removed in favor of exactly this list. Referenced as a
# lightweight anonymous table (not the ORM model) so this migration stays
# valid even if Project's Python shape changes later.
PROJECT_NAMES = ["OBE", "WUT", "RNAP", "BI", "ECMC", "CLU", "DNR", "ADMIN"]

projects_table = sa.table("projects", sa.column("name", sa.String))


def upgrade() -> None:
    op.bulk_insert(projects_table, [{"name": name} for name in PROJECT_NAMES])


def downgrade() -> None:
    op.execute(projects_table.delete().where(projects_table.c.name.in_(PROJECT_NAMES)))
