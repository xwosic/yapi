class Lexicon:
    def __init__(self, conf=None, **kwargs):
        if isinstance(conf, dict):
            kwargs = {**conf, **kwargs}
        elif isinstance(conf, list):
            kwargs = {'conf':conf, **kwargs}

        for k, v in kwargs.items():
            if isinstance(v, dict):
                v = Lexicon(v)
            self.__setattr__(str(k), v)
    
    def __getitem__(self, key: str):
        return self.__dict__.get(key)
    
    def __str__(self):
        result = []
        for k, v in self.__dict__.items():
            result.append(f'{k}: {v}')
        return '\n'.join(result)
    
    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return None
