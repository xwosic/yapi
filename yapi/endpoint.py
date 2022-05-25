from .utils import Lexicon


class Endpoint:
    def __init__(self, conf: dict):
        self.request = Lexicon(conf['request'])
        self.operations = Lexicon(conf['operations'])
        self.response = Lexicon(conf['response'])
    
    def __str__(self):
        result = str(self.request) \
                 + str(self.operations) \
                 + str(self.response)
        return result
        
