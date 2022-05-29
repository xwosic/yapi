from typing import Dict
from .tasks import Task, SQLTask


class Block:
    task_type = Task

    def __init__(self, conf: dict, db, ignore_nulls: bool):
        self.conf = conf
        self.db = db
        self.ignore_nulls = ignore_nulls
        self.tasks = self.create_tasks()
    
    def create_tasks(self):
        tasks: Dict[self.task_type] = {}
        for variable, command_or_options in self.conf.items():
            print('creating', self.task_type, 'type task')
            tasks[variable] = self.task_type(
                variable, 
                command_or_options,
                db=self.db,
                ignore_nulls=self.ignore_nulls
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