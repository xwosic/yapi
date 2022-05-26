from .utils import Lexicon
from fastapi import Depends
from .context import Context


class Endpoint:
    def __init__(self, conf: dict, context: Context):
        self.name = list(conf.keys())[0]
        self.request = Lexicon(conf[self.name].get('request'))
        self.operations = Lexicon(conf[self.name].get('operations'))
        self.response = Lexicon(conf[self.name].get('response'))
        self.description = conf[self.name].get('description')
        self.context = context
        print('endpoint', self.name, 'created')

    def __str__(self):
        result = str(self.request) \
                 + str(self.operations) \
                 + str(self.response)
        return result
    
    def generate_call(self):
        """
        Each step of execution has to pass all
        outcome to next step.
        I see two ways right now:
            1. Create local namespace per execution.
            This requires "supervisor".
            2. Each step takes and returns *args and **kwargs
            This is more complicated but also more straightforward.
            last(second(first(*args, **kwargs)))
        """
        request_model = self.context.models[self.request.model]
        response_model = self.context.models[self.response.model]
        
        if request_model:
            def func(param: request_model = Depends()):
                query = 'select * from users'
                result = self.context.db.execute(query)

                return result
        else:
            def func():
                return self.response
        
        func.__doc__ = self.description if self.description else ""
        return func     
