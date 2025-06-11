from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.engine import Engine
from typing import Any, List


def create_mysql_engine(connection_string: str) -> Engine:
    return create_engine(connection_string)


def reflect_schema(engine: Engine) -> MetaData:
    meta = MetaData()
    meta.reflect(bind=engine)
    return meta


def execute_sql(engine: Engine, sql: str) -> List[Any]:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.fetchall()
