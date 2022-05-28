import re
from typing import Callable, Dict, List, Union
from copy import copy


class Operations:
    def __init__(self, conf: List[Dict[str, str]], context, ns: dict = None):
        self.db = context.db
        self.blocks = self.create_blocks(conf) if conf else []
    
    def create_blocks(self, conf: dict):
        mapping = {
            'sql': SQLBlock,
            'python': PythonBlock,
            'request': RequestBlock
        }
        blocks: List[Block] = []
        for block in conf:
            for block_type, block_config in block.items():
                blocks.append(mapping[block_type](block_config, db=self.db))
        
        return blocks
    
    def execute(self, ns: dict):
        for block in self.blocks:
            ns = block.execute_tasks(ns)
        return ns

class Task:
    options_config = {
        'command_preparation': None,
        'required': []
    }

    def __init__(self, variable: str, options, db) -> None:
        self.variable = variable
        self.db = db
        self.task_type = None  # 'task' / 'task_with_options'
        self.command, self.options = self.recognize_syntax(options)
        self.command = self.create_command()
    
    def recognize_syntax(self, options: Union[str, dict]):
        try:
            if isinstance(options, str):
                # this is variable: command syntax
                self.task_type = 'task'
                return options, None
            elif isinstance(options, (int, float)):
                self.task_type = 'task'
                options = str(options)
                return options, None
            elif isinstance(options, dict):
                # this is variable: {options} syntax
                self.task_type = 'task_with_options'
                return None, options
        except Exception as ex:
            raise ValueError(f'Failed to parse: {self.variable}: {options}. Error: {ex}')
    
    def create_command(self):
        if self.task_type == 'task':
            return self.command
        
        # validate required options
        for option_name in self.options_config['required']:
            if option_name not in self.options:
                raise NotImplementedError(
                    f'Task on variable {self.variable}: '
                    f'{option_name} is required'
                )
            
        if self.options_config['command_preparation'] is None:
            raise NotImplementedError(
                f'Task on variable {self.variable}: '
                f'command_preparation method is required'
            )
        
        command = self.options_config['command_preparation'](self, self.options)
        return command
    
    def convert_python_str_to_sql(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, (list, tuple)):
            return '(' + ', '.join(value) + ')'
        elif isinstance(value, dict):
            k_v_list = [f"{k}={self.convert_python_str_to_sql(v)}" for k, v in value.items()]
            return ', '.join(k_v_list)
    
    def replace_variables_with_values_from_ns(self, ns: dict, command: str):
        result_command = copy(command)
        for k, v in ns.items():
            print(k, '->', v)
            result_command = result_command.replace(k, self.convert_python_str_to_sql(v))
        return result_command
    
    def execute(self, ns: dict):
        if isinstance(self.command, str):
            args = [
                self.command, 
                {}, 
                ns
            ]
            if '=' in self.command:  # to do sth more accurate
                print('executing command:', self.command, 'on', self.variable)
                exec(*args)
            
            else:
                print('evaluating command:', self.command, 'on', self.variable)
                ns[self.variable] = eval(*args)

        elif isinstance(self.command, Callable):
            print('executing method for variable:', self.variable)
            ns[self.variable] = self.command(ns)
        
        return ns


class SQLTask(Task):
    def command_creator(self, options: dict):
        query: str = options['query']
        
        def db_executor(ns: dict):
            nonlocal query
            query_with_values = self.replace_variables_with_values_from_ns(ns, query)
            print(f'executing query: {query_with_values}')
            return self.db.execute(query_with_values)
        
        return db_executor

    options_config = {
        'command_preparation': command_creator,
        'required': ['query']
    }


# class TaskWithOptions(Task):
#     def __init__(self, variable: str, options: dict, ns: dict):
#         self.variable = variable
#         self.options = options
#         self.ns = ns
#         self.command = self.create_command()

#     def create_command(self):
#         raise NotImplementedError('Define command.')

# # query = 'select * from users'
# # result = self.context.db.execute(query)


# class SQLTask(TaskWithOptions):
#     def create_command(self):
#         query: str = self.options.get('query')
#         if query is None:
#             raise NotImplementedError(
#                 '"query" field is required '
#                 'in sql options.'
#             )
#         if not query.startswith('"') \
#            and not query.startswith("'"):
#             query = '"' + query + '"'
        
#         self.command = f'db.execute({query})'
#         print('command created', self.command)


class Block:
    task_type = Task

    def __init__(self, conf: dict, db):
        self.conf = conf
        self.db = db
        self.tasks = self.create_tasks()
    
    def create_tasks(self):
        tasks: Dict[self.task_type] = {}
        for variable, command_or_options in self.conf.items():
            print('creating', self.task_type, 'type task')
            tasks[variable] = self.task_type(
                variable, 
                command_or_options,
                db=self.db
            )

        return tasks
    
    def execute_tasks(self, ns: dict):
        for name, task in self.tasks.items():
            print(self.__class__.__name__, 'start executing task:', name)
            ns = task.execute(ns)
            print('task comleted')   
        return ns     


class SQLBlock(Block):
    task_type = SQLTask


class PythonBlock(Block):
    pass


class RequestBlock(PythonBlock):
    pass