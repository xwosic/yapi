from .db import DB
from .environment import Env
from .model_loader import ModelLoader
from .yaml_config import Yamloader


class Context:
    def __init__(self, yaml_path: str):
        self.config = Yamloader(yaml_path)
        self.models = ModelLoader()
        self.env = Env(self.config['environment'])
        self.db = DB(self.env.connection_string)
