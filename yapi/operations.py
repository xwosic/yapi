import re
from typing import Callable, Dict, List, Union
from copy import copy


class Operations:
    def __init__(self, conf: List[Dict[str, str]], db, ns: dict = None):
        self.db = db
        self.ns = ns if ns else {}
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
                blocks.append(mapping[block_type](block_config, ns=self.ns, db=self.db))
        
        return blocks
    
    def execute(self):
        for block in self.blocks:
            print('ns before:', self.ns)
            block.execute_tasks()
            print('ns after:', self.ns)
        
        return self.ns
    
    def remove_fragile_info_from_result(self):
        result = copy(self.ns)
        result.pop('db')
        return result


class Task:
    options_config = {
        'command_preparation': None,
        'required': []
    }

    def __init__(self, variable: str, options: Union[str, int, dict], ns: dict, db) -> None:
        self.variable = variable
        self.ns = ns
        self.db = db
        self.task_type = None  # 'task' / 'task_with_options'
        self.command, self.options = self.recognize_syntax(options)
        self.command = self.create_command()
    
    def recognize_syntax(self, options: Union[str, dict]):
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
    
    def replace_variables_with_values_from_ns(self, command: str):
        for k, v in self.ns.items():
            print(k, '->', v)
            command = command.replace(k, str(v))
        return command
    
    def execute(self):
        if isinstance(self.command, str):
            args = [
                self.command, 
                {}, 
                self.ns
            ]
            if '=' in self.command:  # to do sth more accurate
                print('executing command:', self.command, 'on', self.variable)
                exec(*args)
            
            else:
                print('evaluating command:', self.command, 'on', self.variable)
                self.ns[self.variable] = eval(*args)

        elif isinstance(self.command, Callable):
            print('executing method for variable:', self.variable)
            self.ns[self.variable] = self.command(self.ns)


class SQLTask(Task):
    def command_creator(self, options: dict):
        query: str = options['query']
        
        def db_executor(ns: dict):
            nonlocal query
            query = self.replace_variables_with_values_from_ns(query)
            print(f'executing query: {query}')
            return self.db.execute(query)
        
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

    def __init__(self, conf: dict, ns: dict, db):
        self.conf = conf
        self.ns = ns
        self.db = db
        self.tasks = self.create_tasks()
    
    def create_tasks(self):
        tasks: Dict[self.task_type] = {}
        for variable, command_or_options in self.conf.items():
            print('creating', self.task_type, 'type task')
            tasks[variable] = self.task_type(
                variable, 
                command_or_options, 
                ns=self.ns,
                db=self.db
            )

        return tasks
    
    def execute_tasks(self):
        for name, task in self.tasks.items():
            print(self.__class__.__name__, 'start executing task:', name)
            task.execute()
            print('task comleted')        


class SQLBlock(Block):
    task_type = SQLTask


class PythonBlock(Block):
    pass


class RequestBlock(PythonBlock):
    pass