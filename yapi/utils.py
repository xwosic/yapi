from copy import copy
from socket import if_indextoname


class book:
    def __init__(self, *args, **kwargs):
        for a in args:
            if isinstance(a, dict):
                kwargs = {**kwargs, **a}

        self.dict_to_book(**kwargs)

    def dict_to_book(self, **kwargs):
        """
        Makes dict more accessible.
        Instead of:
            value = foo['bar']['baz']
        You can do:
            value = foo.bar.baz
        """
        for k, v in kwargs.items():
            if isinstance(v, dict):
                v = book(**v)
            elif isinstance(v, list):
                replace_list = []
                for i in v:
                    if isinstance(i, dict):
                        i = book(**i)
                    replace_list.append(i)
                v = replace_list
            self.__setattr__(str(k), v)
    
    def __getitem__(self, key: str):
        return self.__dict__.get(key)
    
    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return None

    def __str__(self):
        result = []
        for k, v in self.__dict__.items():
            result.append(f'{k}: {v}')
        return '\n'.join(result)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key
            if isinstance(value, book):
                for k in value:
                    yield f'{key}|{k}'
            elif isinstance(value, list):
                for i, element in enumerate(value):
                    if isinstance(element, book):
                        for k in element:
                            yield f'{key}|[{i}]|{k}'
    

