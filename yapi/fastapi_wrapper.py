from fastapi import FastAPI


def wrapp_fastapi(app: FastAPI, url_mapping: dict):
    """
    This function starts FastAPI service
    and maps urls to methods.
    url_mapping = {
        'get': {
            'url': method (callable)
        }
    }
    """
    for http_method, urls_methods in url_mapping.items():
        for url, method in urls_methods.items():
            fastapi_method_wrapper = app.__getattribute__(http_method)
            fastapi_method_wrapper(url)(method)
    
    return app
