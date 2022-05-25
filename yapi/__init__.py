from fastapi import FastAPI
from .fastapi_wrapper import wrapp_fastapi
from .yaml_config import Yamloader
from .endpoint import Endpoint


def fake_get() -> str:
    print('fake get')
    return 'hej'


test_mapping = {
        'get': {
            '/users': fake_get
        }
    }


class Yapp(FastAPI):
    def __init__(self, yaml, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Yamloader(path=yaml)
        self.mapping = self.get_method_url_mapping()
        self = wrapp_fastapi(self, test_mapping)
    
    def get_method_url_mapping(self):
        mapping = {
            'get': {},
            'post': {},
            'put': {},
            'delete': {}
        }
        for method_url in self.config['api']:
            method, url = method_url.split(' ')
            mapping[method][url] = Endpoint(self.config['api'][method_url])
        print(mapping)
        return mapping
