from yapi.fastapi_wrapper import wrapp_fastapi

def fake_get() -> str:
    print('fake get')
    return 'hej'


test_mapping = {
        'get': {
            '/users': fake_get
        }
    }


app = wrapp_fastapi(test_mapping)
