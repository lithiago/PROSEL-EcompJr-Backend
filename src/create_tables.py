from __future__ import annotations

from sqlalchemy import Engine

import src.models
from src.database import engine
from src.models.base import Base


def create_tables(database_engine: Engine = engine) -> None:
    Base.metadata.create_all(bind=database_engine)


if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas ou já existentes no banco configurado.")
