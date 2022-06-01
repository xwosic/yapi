from fastapi import Depends
from pydantic import BaseModel
from typing import Optional
from .request import YappRequest


class YappResponse(YappRequest):
    """
    YappResponse:
    * uses models from models.py
    * takes from endpoint's namespace defined values
    and retuns them to client
    * if not defined - returns everything from ns
    * if variable defined - returns variable
    * if model defined - returns model or list of models
    """
    def __init__(self, conf: dict, context) -> None:
        self.models = context.models
        self.response_model = None
        self.response_variable = None
        if conf:
            self.response_model = self.get_model(conf)
            self.model_fields = self.set_fields(self.response_model)
            self.response_variable = self.get_variable(conf)
            if self.response_model and self.response_variable:
                raise ValueError('Error in response config:'
                                 'Define response model XOR variable.')
    
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
        else:
            return ns