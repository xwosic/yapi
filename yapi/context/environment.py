import os


class Env:
    def __init__(self, env_config: list):
        for variable in env_config:
            if isinstance(variable, str):
                # get variable from env
                value = os.environ[variable]
                self.__setattr__(variable, value)

            elif isinstance(variable, dict):
                for k, v in variable.items():
                    os.environ[k] = v
                    self.__setattr__(k, v)                
