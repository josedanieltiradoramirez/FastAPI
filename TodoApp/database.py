import os

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todosapp.db")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def ensure_sqlite_column(engine, table_name: str, column_name: str, column_type_sql: str) -> None:
    """
    SQLite: `create_all()` no modifica tablas existentes.
    Este helper agrega una columna si falta, preservando los datos.
    """
    if engine.dialect.name != "sqlite":
        return

    with engine.connect() as conn:
        rows = conn.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
        existing_columns = {row[1] for row in rows}  # row[1] = column name
        if column_name in existing_columns:
            return

        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_sql}"))
        conn.commit()
