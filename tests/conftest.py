"""Shared pytest fixtures/setup for every tier under tests/.

Points DATABASE_URL at a dedicated *test* database (never the dev one you'd
lose data in), reachable via localhost — tests run on the host, not inside
the docker-compose network, so the `db` hostname the api container uses
doesn't resolve here. Creates that database if it doesn't exist, applies
migrations, then truncates it between tests so each test starts clean.
"""

import os
import subprocess
from pathlib import Path

import psycopg
import pytest
from dotenv import dotenv_values
from sqlalchemy import create_engine, text

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
env = dotenv_values(REPO_ROOT / ".env")

_HOST = "localhost"
_PORT = env.get("POSTGRES_PORT", "5432")
_USER = env["POSTGRES_USER"]
_PASSWORD = env["POSTGRES_PASSWORD"]
_TEST_DB = f"{env['POSTGRES_DB']}_test"

admin_conn = psycopg.connect(
    f"postgresql://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/postgres", autocommit=True
)
with admin_conn.cursor() as cur:
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (_TEST_DB,))
    if cur.fetchone() is None:
        cur.execute(f'CREATE DATABASE "{_TEST_DB}"')
admin_conn.close()

os.environ["DATABASE_URL"] = f"postgresql+psycopg://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_TEST_DB}"

subprocess.run(
    [str(BACKEND_DIR / ".venv" / "bin" / "alembic"), "upgrade", "head"],
    cwd=BACKEND_DIR,
    check=True,
)

_engine = create_engine(os.environ["DATABASE_URL"])


@pytest.fixture(autouse=True)
def _clean_database():
    yield
    with _engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE tasks, projects RESTART IDENTITY CASCADE"))
