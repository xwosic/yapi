from fastapi import FastAPI, Depends
from .endpoint import Endpoint
from .context import Context


class Yapp(FastAPI):
    def __init__(self, yaml, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = Context(yaml)
        self.mapping = self.map_url_to_method()
        self = Yapp.wrapp_fastapi(self, self.mapping)
    
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
        for method_url in self.context.config['api']:
            endpoint = Endpoint(method_url, self.context)
            method, url = method_url.split(' ')
            mapping[method][url] = endpoint.call
        return mapping
    
    @staticmethod
    def wrapp_fastapi(app: FastAPI, url_mapping: dict):
        """
        Adds endpoints to app using prepared mapping.
        This is equivalent to:

        app = FastAPI()

        @app.get('/foo')
        def bar():
            return 'baz'
        """
        def foo():
            print('var')
            return 'bar'

        for http_method, urls_methods in url_mapping.items():
            for url, method in urls_methods.items():
                fastapi_method_wrapper = app.__getattribute__(http_method)
                fastapi_method_wrapper(url, dependencies=[Depends(foo)])(method)
        
        return app
