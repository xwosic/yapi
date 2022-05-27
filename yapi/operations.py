from typing import Dict, List


class Operations:
    def __init__(self, conf: List[Dict[str, str]], ns: dict = None):
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
                blocks.append(mapping[block_type](block_config, ns=self.ns))
        
        return blocks
    
    def execute(self):
        for block in self.blocks:
            block.execute_tasks()
        
        return self.ns


class Task:
    def __init__(self, variable: str, command: dict, ns: dict) -> None:
        self.variable = variable
        self.command = command
        self.ns = ns
    
    def execute(self):
        args = [
            self.command, 
            {}, 
            self.ns
        ]
        if '=' in self.command:  # to do sth more accurate
            exec(*args)
        
        else:
            self.ns[self.variable] = eval(*args)


class Block:
    task_type = Task

    def __init__(self, conf: dict, ns: dict):
        self.conf = conf
        self.ns = ns
        self.tasks = self.create_tasks()
    
    def create_tasks(self):
        tasks: Dict[self.task_type] = {}
        for variable, command_or_options in self.conf.items():
            print('creating', self.task_type, 'type task')
            tasks[variable] = self.task_type(
                variable, 
                command_or_options, 
                ns=self.ns
            )

        return tasks
    
    def execute_tasks(self):
        for name, task in self.tasks.items():
            print('start executing task:', name)
            task.execute()
            print('task comleted')


class TaskWithOptions(Task):
    def __init__(self, variable: str, options: dict, ns: dict):
        self.variable = variable
        self.options = options
        self.ns = ns
        self.command = self.create_command()

    def create_command(self):
        raise NotImplementedError('Define command.')

# query = 'select * from users'
# result = self.context.db.execute(query)

class SQLTask(TaskWithOptions):
    def create_command(self):
        query: str = self.options.get('query')
        if query is None:
            raise NotImplementedError(
                '"query" field is required '
                'in sql options.'
            )
        if not query.startswith('"') \
           and not query.startswith("'"):
            query = '"' + query + '"'
        
        self.command = f'db.execute({query})'
        print('command created', self.command)
        


class SQLBlock(Block):
    task_type = SQLTask


class PythonBlock(Block):
    pass


class RequestBlock(PythonBlock):
    pass