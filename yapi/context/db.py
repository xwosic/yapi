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
    
    def execute(self, query: str):
        lower_query = query.lower()
        no_result = [
            'create',
            'delete', 
            'insert',
            'update'
        ]
        try:
            in_query = []
            for clause in no_result:
                if clause in lower_query:
                    in_query.append(True)
                else:
                    in_query.append(False)
            if any(in_query):
                with self.engine.connect() as conn:
                    conn.execute(query)
            
            else:
                with self.engine.connect() as conn:
                    cursor = conn.execute(query)
                    result = cursor.fetchall()
                    return [row._asdict() for row in result]

        except Exception as ex:
            print(f'execution of: {query} failed because of {ex}')
            raise
    
    def get_columns(self, table: str):
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table)
        return [column['name'] for column in columns]
