from .db import DB
from .dependency_loader import DependenciesLoader
from .environment import Env
from .model_loader import ModelLoader
from .yaml_config import Yamloader


class Context:
    def __init__(self, yaml_path: str):
        self.config = Yamloader(yaml_path)
        self.models = ModelLoader()
        self.dependencies = DependenciesLoader()
        self.env = Env(self.config['environment'])
        self.db = DB(self.env.connection_string)
