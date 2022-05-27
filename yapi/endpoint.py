from .utils import book
from fastapi import Depends
from .context import Context
from .operations import Operations


class Endpoint:
    def __init__(self, method_url: str, context: Context):
        self.name = method_url
        print(self.name, ' -> endpoint init')
        self.context = context
        self.request = book(self.context.config['api'][self.name].get('request'))
        namespace = {'db': self.context.db}
        self.operations = Operations(conf=self.context.config['api'][self.name].get('operations'))
        self.response = book(self.context.config['api'][self.name].get('response'))
        self.description = self.context.config['api'][self.name].get('description')
        print(self.name, ' -> endpoint call generation')
        self.generated_function = self.generate_call()
        print(self.name, ' -> endpoint created')

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
                result = self.operations.execute()

                return result
        else:
            def func():
                return self.operations.execute()
        
        func.__doc__ = self.description if self.description else ""
        return func   

    @property
    def call(self):
        return self.generated_function
