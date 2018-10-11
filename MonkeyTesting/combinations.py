from .schema_types import types
from voluptuous import Schema
data_schema = Schema({'size': int, 'content': str})

test_schema = Schema({'version': str,
                      'data': Schema({'size': int, 'content': str})}
                      )
