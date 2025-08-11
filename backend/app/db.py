from __future__ import annotations
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from .config import settings

_connection_pool: pool.SimpleConnectionPool | None = None


def get_connection_pool() -> pool.SimpleConnectionPool:
    global _connection_pool
    if _connection_pool is None:
        dsn = (
            f"host={settings.db_host} "
            f"port={settings.db_port} "
            f"dbname={settings.db_name} "
            f"user={settings.db_user} "
            f"password={settings.db_password}"
        )
        _connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn)
    return _connection_pool


@contextmanager
def get_db_conn():
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


@contextmanager
def get_db_cursor():
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            yield cur