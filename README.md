# yapi (WORK IN PROGRESS)
yaml to fastapi parser

## how to use it
### folder structure
```
some_project_dir/
                /main.py
                /models.py
                /yapi.yaml
```

let's define GET endpoint with url /foo/{bar_id}
```yaml
# yapi.yaml
api:
    get /foo/{bar_id}:
        description: endpoint description visible to client
        request:
            model: FooModel
        operations:
            - sql: 
                db_result:
                    query: select * from foo_table
            - python:
                endpoint_response: parse_response(db_result)
        response:
            model: FooResponseModel

```
all you need to do in main.py is:
```python
# main.py

from yapi import Yapp

app = Yapp('yapi.yaml')

```
and in models.py there should be two models:
```python
# models.py

from datetime import datetime
from fastapi import Query, Body
from pydantic import BaseModel

class FooModel(BaseModel):
    # params from url will be mapped to this variable
    bar_id: int
    # query params should use Query class
    username: str = Query(None)
    # params in body
    baz: float = Body(1.23)


class FooResponseModel(BaseModel):
    bar_id: int
    usermane: str
    birth_date: datetime

```

in terminal run:
``` shell
python -m uvicorn main:app
```