from voluptuous import Schema
import random
from typing import Union
import typing
from types import GeneratorType
from schema_types import types
from schema_types import enum_of_types
import requests
data_schema = Schema({'size': int, 'content': str})

test_schema = Schema({'version': str,
                      'data': Schema({'size': int, 'content': str, 'neco': bool} 
                      ), 'name': str})

def unwrap_schema(schema: Schema)-> Union[list, dict]:
    return schema.schema

def create_random_api_request(schema):
    request = {}
    for key, value in unwrap_schema(schema).items():
        # print(unwrap_schema(schema).items())
        # print(f'{key} : {value}')
        # print(type(value))
        #print(type(value))
        if value == str:
            request[key] = ''
            for i in range(0,random.randint(0,30)):
                request[key] += chr(random.randint(32, 500))
        elif value == int:
            request[key] = random.randint(0,4000000) - 2000000
        elif value == float:
            request[key] = (random.randint(0,10000000) - 50000000)/100000
        # elif value == dict:
        #     #print('dict ok')
        #     request[key] = create_api_request(value)
        elif isinstance(value, Schema):
            #print('dict ok')
            request[key] = create_random_api_request(value)
    #print('request: ' + str(request))
    return request


def get_list_for_generator(schema: Union[Schema,list, dict]) -> tuple:
    ''' return tuple ([data_types],[keys])'''
    list_of_attributtes = []
    list_of_keys = {}
    if isinstance(schema, Schema):
        schema = unwrap_schema(schema)
    for key, value in schema.items():
        if isinstance(value, Schema):
            value = unwrap_schema(value)
        if type(value) is dict:
            attr, keys = get_list_for_generator(value)
            list_of_attributtes.append(attr)
            list_of_keys[key] = keys
        elif value in enum_of_types:
            list_of_attributtes.append(value)
            list_of_keys[key] = 'end'
    return list_of_attributtes, list_of_keys

def get_orders(parsed_schema):
    """return list_of_orders for behaving indicies like numbers"""
    orders = []
    for t in parsed_schema:
        if type(t) == list:
            orders.append(get_orders(t))
        elif t in enum_of_types:
            orders.append(len(enum_of_types[t]))
    return orders


def generate_default_state(orders):
    state = []
    for order in orders:
        if type(order) == list:
            state.append(generate_default_state(order)) 
        else:
            state.append(0)
    return state

def generate_default_carry_state(orders):
    state = []
    for order in orders:
        state.append(0)
    return state

def count_of_variations(orders):
    count = 1
    for order in orders:
        if type(order) == list:
            count *= count_of_variations(order) 
        else:
            count *= order
    return count

def make_generator(order):
    if type(order) == list:
        for i in kombinations(order):
            yield i
    else:
        for i in range(order):
            yield i

def generate_1d_orders(orders):
    temp = []
    for order in orders:
        if type(order) != list:
            temp.append(order)
        else:
            temp.append(count_of_variations(order))
    return temp

def nd_to_1d(orders, index=0):
    """return 1d_repr. and map"""
    _1d_representation = []
    map = []
    for i ,order in enumerate(orders):
        if type(order) == list:
            rep, m = nd_to_1d(order, i)
            for r in rep:
                _1d_representation.append(r)
            map.append(m)
        else:
            _1d_representation.append(order)
            map.append(i + index)
    return _1d_representation, map

def _1d_to_nd(_1d_representation, map):
    orders = []
    for ind in map:
        if type(ind) == list:
            orders.append(_1d_to_nd(_1d_representation, ind))
        else:
            orders.append(_1d_representation[ind])
    return orders

def kombinations(orders):
    carry = generate_default_carry_state(orders)
    orders_1d = generate_1d_orders(orders)
    kombination = []
    output = generate_default_state(orders)
    for ind in range(len(orders)):
        kombination.append(make_generator(orders[ind]))


    all_carry = False
    #while not all_carry:
    ## first iter
    for ind in range(len(kombination)):
        output[ind] = next(kombination[ind])
    yield output

    for number in range(count_of_variations(orders) - 1):
        for ind in range(len(kombination)):
            if carry[ind] == 1:
                kombination[ind] = make_generator(orders[ind])
                output[ind] = next(kombination[ind])
                carry[ind] = 0
                for c_ind in range(ind + 1, len(carry)):
                    if carry[c_ind] == 1:
                        kombination[c_ind] = make_generator(orders[ind])
                        output[c_ind] = next(kombination[c_ind])
                        carry[c_ind] = 0
                    else:
                        output[c_ind] = next(kombination[c_ind])

                        if output[c_ind] == (orders[c_ind] - 1):
                            carry[c_ind] = 1
                        break
                yield output
                break

            else:
                output[ind] = next(kombination[ind])
                if output[ind] == (orders[ind] - 1):
                    carry[ind] = 1
                yield output
                break
def make_payload(kombination: list, keys: dict, data_types: list) -> list:
    payload = {}

    for ind, key in enumerate(keys):
        if type(kombination[ind]) is not list:
            temp = enum_of_types[data_types[ind]][kombination[ind]]() 
            payload[key] = temp
        else:
            payload[key] = make_payload(kombination[ind], keys[key], data_types[ind])
    
    return payload
        
def nd_kombinations(schema : Schema) -> list:
    """generator for kombinations of data"""
    data_types, keys = get_list_for_generator(test_schema)
    orders = get_orders(data_types)
    print(keys)
    print(data_types)
    _1d, map = nd_to_1d(orders)
    for k in kombinations(_1d):
        yield make_payload(_1d_to_nd(k, map), keys, data_types)

def test_api(schema : Schema, url: str) -> None:
    for data in nd_kombinations(schema):
        response = requests.post(url, json=data)

if __name__ == "__main__":
    for v in nd_kombinations(test_schema):
        print(v)

