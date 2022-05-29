from typing import Dict, List
from .blocks import Block, SQLBlock, PythonBlock, RequestBlock


class Operations:
    def __init__(self, conf: List[Dict[str, str]], context, ns: dict = None):
        self.db = context.db
        self.ignore_nulls = context.operations_kwargs['ignore_nulls']
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
                blocks.append(
                    mapping[block_type](block_config,
                                        db=self.db,
                                        ignore_nulls=self.ignore_nulls)
                )
        
        return blocks
    
    def execute(self, ns: dict):
        for block in self.blocks:
            ns = block.execute_tasks(ns)
        return ns
