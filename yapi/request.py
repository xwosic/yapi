from typing import Optional
from fastapi import Depends
from pydantic import BaseModel


class YappRequest:
    """
    * it has to return request model
    * it has to return dependencies
    * it has to put dependencies into call's signature 
        and put dependency result inside namespace
    * it has to convert model to namespace dict 
        {
            'params.param_1': ..., 
            or
            '<model_name>.param_2': ...
        }
    * perform extra validation INSIDE endpoint call
    """
    def __init__(self, conf: dict, context) -> None:
        self.models = context.models
        self.context_dependencies = context.dependencies
        self.request_model = None
        self.dependencies = None
        if conf:
            self.request_model = self.get_model(conf)
            self.dependencies = self.get_dependencies(conf)
    
    def get_model(self, conf: dict) -> Optional[BaseModel]:
        """
        Maps model name from request config to model
        from models.py
        """
        model_name = conf.get('model')
        if model_name:
            try:
                model = self.models[model_name]
            except KeyError:
                raise ValueError(f'There is no {model_name}'
                                 ' in models.py')
            return model
    
    def get_dependencies(self, conf: dict):
        """
        Maps dependency name to method in dependencies.
        Returns mapping:
            {
                "variable_name": Depends(method)
            }
        """
        deps = conf.get('dependencies')
        if deps:
            result = {}
            for variable, dependency_name in deps.items():
                try:
                    dependency_method = self.context_dependencies[dependency_name]
                except KeyError:
                    raise ValueError(f'There is no {dependency_name}'
                                     ' in dependencies.py')
                result[variable] = Depends(dependency_method)
            return result
    
    def put_params_to_ns(self, input_params: BaseModel, ns: dict) -> dict:
        model_name = type(input_params).__name__
        print('add model to request', model_name)
        for k, v in input_params.dict().items():
            ns[f'{model_name}.{k}'] = v
        print(ns)
        return ns
    
    def put_dependency_results_to_ns(self):
        pass

    def extra_validation(self):
        pass