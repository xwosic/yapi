from fastapi import Depends
from pydantic import BaseModel
from typing import Optional


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
        self.ignore_nulls = False
        if conf:
            self.request_model = self.get_model(conf)
            self.dependencies = self.get_dependencies(conf)
            context.operations_kwargs = {'ignore_nulls': self.ignore_nulls}
            print(context.operations_kwargs)
    
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
            
            for v in model.__fields__.values():
                if not v.required:
                    self.ignore_nulls = True
                    break
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
            result = []
            for dependency_name in deps:
                try:
                    dependency_method = self.context_dependencies[dependency_name]
                except KeyError:
                    raise ValueError(f'There is no {dependency_name}'
                                     ' in dependencies.py')
                result.append(Depends(dependency_method))
            return result
    
    def put_params_to_ns(self, input_params: BaseModel, ns: dict) -> dict:
        """
        Converts request params to dict and adds
        them to enpoint's execution namespace.
        """
        model_name = type(input_params).__name__
        for k, v in input_params.dict().items():
            ns[f'{model_name}.{k}'] = v
        return ns

    def extra_validation(self):
        pass