# get all model classes from models
try:
    from models import *

except ImportError:
    raise NotImplementedError(
        'No models.py found in main directory. '
        'Create file "models.py".')


class ModelLoader:
    def __init__(self):
        self.models = self.load_models()
    
    def load_models(self) -> dict:
        """
        Gets all defined objects from models.py"""
        import models as models
        imported_models = {}
        namespace = globals()
        for d in dir(models):
            if d.startswith('_') or d.endswith('_'):
                continue
            imported_models[d] = namespace[d]
        
        return imported_models
    
    def __getitem__(self, key: str):
        return self.models[key]
