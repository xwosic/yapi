# get all model classes from dependencies
try:
    from dependencies import *

except ImportError:
    pass


class DependenciesLoader:
    def __init__(self):
        self.dependencies = self.load_dependencies()
    
    def load_dependencies(self) -> dict:
        """
        Gets all defined objects from dependencies.py"""
        try:
            import dependencies
        except ImportError:
            return None

        imported_dependencies = {}
        namespace = globals()
        for d in dir(dependencies):
            if d.startswith('_') or d.endswith('_'):
                continue
            imported_dependencies[d] = namespace[d]
        return imported_dependencies
    
    def __getitem__(self, key: str):
        return self.dependencies[key]
