from fastapi import FastAPI
from .fastapi_wrapper import wrapp_fastapi


def fake_get() -> str:
    print('fake get')
    return 'hej'


test_mapping = {
        'get': {
            '/users': fake_get
        }
    }


class Yapp(FastAPI):
    def __init__(self, *args, yaml=None, **kwargs):
        super().__init__(*args, **kwargs)
        self = wrapp_fastapi(self, test_mapping)
