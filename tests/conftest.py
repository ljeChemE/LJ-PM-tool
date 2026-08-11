"""Shared pytest fixtures/setup for every tier under tests/.

Points DATABASE_URL at Postgres via localhost (tests run on the host, not
inside the docker-compose network, so the `db` hostname the api container
uses doesn't resolve here) before anything imports the app.
"""

import os
from pathlib import Path

from dotenv import dotenv_values

REPO_ROOT = Path(__file__).resolve().parent.parent
env = dotenv_values(REPO_ROOT / ".env")

os.environ["DATABASE_URL"] = (
    f"postgresql://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}"
    f"@localhost:{env.get('POSTGRES_PORT', '5432')}/{env['POSTGRES_DB']}"
)
