from os import strerror
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


class Block:
    def __init__(self, conf: dict, ns: dict):
        self.conf = conf
        self.ns = ns
        self.tasks = self.create_tasks()
    
    def create_tasks(self):
        tasks: Dict[Task] = {}
        for variable, command in self.conf.items():
            tasks[variable] = Task(variable, command, ns=self.ns)

        return tasks
    
    def execute_tasks(self):
        for task in self.tasks.values():
            task.execute()


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
        if '=' in self.command:
            exec(*args)
        
        else:
            self.ns[self.variable] = eval(*args)


class TaskWithOptions(Task):
    def __init__(self, variable: str, options: str, ns: dict):
        self.variable = variable
        self.options = options
        self.ns = ns
        self.command = self.create_command()

    def create_command(self):
        raise NotImplemented('Define command.')

# query = 'select * from users'
# result = self.context.db.execute(query)
class SQLBlock(Block):
    pass


class PythonBlock(Block):
    pass


class RequestBlock(PythonBlock):
    pass