from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine


class DB:
    def __init__(self,
                 connection_str: str,
                 connection_args: dict = None):

        required_args = {'check_same_thread': False}

        if connection_args is not None:
            required_args = {**required_args, **connection_args}

        self.engine: Engine = create_engine(connection_str, 
                                            connect_args=required_args)
    
    def execute(self, query: str, commit=True):
        with self.engine.connect() as conn:
            cursor = conn.execute(query, commit=commit)
            return cursor.fetchall()
    
    def get_columns(self, table: str):
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table)
        return [column['name'] for column in columns]
