from .utils import Lexicon


class Endpoint:
    def __init__(self, conf: dict):
        self.request = Lexicon(conf['request'])
        self.operations = Lexicon(conf['operations'])
        self.response = Lexicon(conf['response'])
        self.int = int
    
    def __str__(self):
        result = str(self.request) \
                 + str(self.operations) \
                 + str(self.response)
        return result
    
    def generate_call(self):
        def func(param: self.int):
            print(param)
            print(self.operations)
            return self.response
        return func     
