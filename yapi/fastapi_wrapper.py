from fastapi import FastAPI


def wrapp_fastapi(url_mapping):
    """
    This function starts FastAPI service
    and maps urls to methods.
    url_mapping = {
        'get': {
            'url': method (callable)
        }
    }
    """
    app = FastAPI()

    # map urls to methods
    for http_method, urls_methods in url_mapping.items():
        for url, method in urls_methods.items():
            fastapi_method_wrapper = app.__getattribute__(http_method)
            fastapi_method_wrapper(url)(method)
    
    return app
