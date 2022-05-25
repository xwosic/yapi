from fastapi import FastAPI
from .fastapi_wrapper import wrapp_fastapi
from .yaml_config import Yamloader
from .endpoint import Endpoint


class Yapp(FastAPI):
    def __init__(self, yaml, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Yamloader(path=yaml)
        self.mapping = self.map_url_to_method()
        self = wrapp_fastapi(self, self.mapping)
    
    def map_url_to_method(self):
        """
        Create mapping used to wrapp fastapi app
        in yapi app.
        Splits "get /foo/bar" -> "get" and "/foo/bar".
        Then parses yaml into an endpoint which is used
        to generate server's response function.
        """
        mapping = {
            'get': {},
            'post': {},
            'put': {},
            'delete': {}
        }
        for method_url in self.config['api']:
            method, url = method_url.split(' ')
            endpoint = Endpoint({method_url: self.config['api'][method_url]})
            mapping[method][url] = endpoint.generate_call()
        return mapping
