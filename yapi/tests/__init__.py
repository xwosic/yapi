from ..context.yaml_config import Yamloader
from ..context.db import DB


def get_yaml(path: str):
    yaml = Yamloader(path)
    return yaml


def get_memory_engine(path: str) -> DB:
    db = DB(connection_str=f'sqlite:///{path}')
    return db
