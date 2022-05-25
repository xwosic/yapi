from .utils import Lexicon


class Endpoint:
    def __init__(self, conf: dict):
        self.name = list(conf.keys())[0]
        self.request = Lexicon(conf[self.name]['request'])
        self.operations = Lexicon(conf[self.name]['operations'])
        self.response = Lexicon(conf[self.name]['response'])
        self.int = int
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
        def func(param: self.int):
            """
            here is your description
            """
            print(param)
            print(self.operations)
            return self.response
        return func     
