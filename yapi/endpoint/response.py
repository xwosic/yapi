"""
#usage

```yaml
<not in config> -> return null

response: -> return null

response: ~ -> return null

response: null -> return null

response:
    model: SomeModel -> return one or list of models

response:
    variable: variable_name -> return VALUE of variable from namespace

response:
    variable: foo
    model: bar -> raise implementation error

```
"""

from pydantic import BaseModel
from typing import Optional
from .request import YappRequest


class YappResponse(YappRequest):
    """
    YappResponse:
    * uses models from models.py
    * takes from endpoint's namespace defined values
    and retuns them to client
    """
    def __init__(self, conf: dict, context) -> None:
        self.models = context.models
        self.response_model = None
        self.response_variable = None
        self.return_all = False
        self.to_return = None
        if conf:
            if isinstance(conf, dict):
                self.response_model = self.get_model(conf)
                self.model_fields = self.set_fields(self.response_model)
                self.response_variable = self.get_variable(conf)
                if self.response_model and self.response_variable:
                    raise ValueError('Error in response config:'
                                     'Define response model XOR variable.')
            else:
                if conf == 'all':
                    self.return_all = True
                else:
                    self.to_return = conf
    
    def set_fields(self, model: Optional[BaseModel]):
        if model:
            return set(self.response_model.__fields__.keys())
        else:
            return None
    
    def key_in_model_fields(self, key: str):
        return key in self.model_fields


    def get_variable(self, conf: dict):
        variable = conf.get('variable')
        if not isinstance(variable, (type(None), str)):
            raise TypeError(f'Error in response config: name of'
                            f'variable has to be of type string. '
                            f'Not {type(variable)}')
        return variable
    
    def filter_response_from_ns(self, ns: dict):
        if self.response_model:
            # search for model instance
            # or list of model instances
            result = []
            for value in ns.values():
                if isinstance(value, dict):
                    try:
                        result = self.response_model.parse_obj(value)
                    except:
                        pass
                elif isinstance(value, list):
                    for v in value:
                        try:
                            result.append(self.response_model.parse_obj(v))
                        except Exception:
                            break
            return result
        elif self.response_variable:
            # search ns for variable
            # with name from config
            if self.response_variable in ns:
                return ns[self.response_variable]
        elif self.return_all:
            return ns
        elif self.to_return:
            return self.to_return
        else:
            return None