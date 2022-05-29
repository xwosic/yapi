from .context import Context
from .endpoint import Endpoint
from fastapi import FastAPI


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
        Then parses yaml into an endpoint and dependencies
        which are used to generate server's response function.
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
            mapping[method][url] = {
                'call': endpoint.call,
                'dependencies': endpoint.request.dependencies
            }
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
        for http_method, urls_methods in url_mapping.items():
            for url, endp_deps in urls_methods.items():
                fastapi_method_wrapper = app.__getattribute__(http_method)
                fastapi_method_wrapper(
                    url, 
                    dependencies=endp_deps['dependencies']
                )(endp_deps['call'])
        
        return app
