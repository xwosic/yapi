import pytest
import os
from pathlib import Path
from ..tasks import Task, SQLTask
from ...tests import get_yaml, get_memory_engine

test_db_path = Path().joinpath(Path(__file__).parent, 'test_db_tasks.db')
test_conf = get_yaml(Path().joinpath(Path(__file__).parent, 'test_operations.yaml'))

# create test table
db = get_memory_engine(test_db_path)
queries = [
    """
    create table test_operations (
    id integer primary key,
    name varchar(255),
    age int
    )
    ;
    """,
    """
    insert into test_operations (name, age)
    values 
        ('a', 1),
        ('b', 2),
        ('c', 3)
    ;
    """,
    """
    select * from test_operations
    """
]

for q in queries:
    db.execute(q)


@pytest.fixture
def sqltask() -> SQLTask:
    def creator(task_conf_name: str):
        conf = test_conf[task_conf_name]
        variable = list(conf.keys())[0]
        options = list(conf.values())[0]
        return SQLTask(variable=variable, options=options, db=db)
    return creator


@pytest.mark.order(1)
def test_sql_task(sqltask: Task):
    ns = {}
    task = sqltask('test_sql_task')
    ns = task.execute(ns)
    assert ns == {'result': [{'age': 1, 'id': 1, 'name': 'a'},
                             {'age': 2, 'id': 2, 'name': 'b'},
                             {'age': 3, 'id': 3, 'name': 'c'}]}


@pytest.mark.order(2)
def test_sql_where(sqltask: Task):
    ns = {}
    task = sqltask('test_sql_where')
    ns = task.execute(ns)
    assert ns == {'result': [{'age': 1, 'id': 1, 'name': 'a'}]}


@pytest.mark.order(3)
def test_sql_add(sqltask: Task):
    ns = {}
    task = sqltask('test_sql_add')
    ns = task.execute(ns)
    assert ns == {'result': None}
    task = sqltask('test_sql_task')
    ns = task.execute(ns)
    assert ns == {'result': [{'age': 1, 'id': 1, 'name': 'a'},
                             {'age': 2, 'id': 2, 'name': 'b'},
                             {'age': 3, 'id': 3, 'name': 'c'},
                             {'age': 4, 'id': 4, 'name': 'd'}]}


@pytest.mark.order(4)
def test_sql_update(sqltask: Task):
    ns = {}
    task = sqltask('test_sql_update')
    ns = task.execute(ns)
    assert ns == {'result': None}
    task = sqltask('test_sql_task')
    ns = task.execute(ns)
    assert ns == {'result': [{'age': 1, 'id': 1, 'name': 'a'},
                             {'age': 2, 'id': 2, 'name': 'b'},
                             {'age': 3, 'id': 3, 'name': 'c'},
                             {'age': 5, 'id': 4, 'name': 'e'}]}


@pytest.mark.order(5)
def test_sql_delete(sqltask: Task):
    ns = {}
    task = sqltask('test_sql_delete')
    ns = task.execute(ns)
    assert ns == {'result': None}
    task = sqltask('test_sql_task')
    ns = task.execute(ns)
    assert ns == {'result': [{'age': 1, 'id': 1, 'name': 'a'},
                             {'age': 2, 'id': 2, 'name': 'b'},
                             {'age': 3, 'id': 3, 'name': 'c'}]}
                             

@pytest.mark.order(-1)
def test_drop_table():
    os.remove(test_db_path)
