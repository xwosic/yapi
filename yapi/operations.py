from os import strerror
from typing import Dict, List


class Operations:
    def __init__(self, conf: List[Dict[str, str]], ns: dict = None):
        if conf:
            self.ns = ns if ns else {}
            self.blocks = self.create_blocks(conf)
    
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
        results = []
        for block in self.blocks:
            results.append(block.execute_tasks())
        
        return results


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
        results = {}
        for variable, task in self.tasks.items():
            results[variable] = task.execute()
        return results


class Task:
    def __init__(self, variable: str, command: dict, ns: dict) -> None:
        self.variable = variable
        self.command = command
        self.ns = ns
    
    def execute(self):
        return eval(self.command, self.ns)


class TaskWithOptions(Task):
    def __init__(self, variable: str, options: str, ns: dict):
        self.variable = variable
        self.options = options
        self.ns = ns
        self.command = self.create_command()

    def create_command(self):
        raise NotImplemented('Define command.')


class SQLBlock(Block):
    pass


class PythonBlock(Block):
    pass


class RequestBlock(PythonBlock):
    pass