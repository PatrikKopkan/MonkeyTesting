from voluptuous import Schema
import random
from typing import Union
import typing
from schema_types import types
from schema_types import enum_of_types
data_schema = Schema({'size': int, 'content': str})

test_schema = Schema({'version': str,
                      'data': Schema({'size': int, 'content': str})}
                      )

test_schema = Schema({'version': str, 'data': int, 'neco': str})

def unwrap_schema(schema: Schema)-> Union[list, dict]:
    return schema.schema

def create_request(schema):
    pass

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
    ''' return list for generator function'''
    list_of_attributtes = []
    list_of_keys = []
    if isinstance(schema, Schema):
        schema = unwrap_schema(schema)
    for key, value in schema.items():
        if isinstance(value, Schema):
            value = unwrap_schema(value)
        if type(value) is dict:
            attr, keys = get_list_for_generator(value)
            list_of_attributtes.append(attr)
            list_of_keys.append(keys)
        elif value in enum_of_types:
            list_of_attributtes.append(value)
            list_of_keys.append(key)
    return list_of_attributtes, list_of_keys

def get_orders(parsed_schema):
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

def count_of_variations(orders):
    count = 1
    for order in orders:
        if type(order) == list:
            count *= count_of_variations(order) 
        else:
            count *= order
    return count

def onestep(ind, carry, variation, orders):
    if carry[ind] == 1:
        variation[ind] = 0
        carry[ind] = 0
        for c_ind in range(ind + 1, len(carry)):
            if carry[c_ind] == 1:
                variation[c_ind] = 0
                carry[c_ind] = 0
            else:
                variation[c_ind] += 1
                if variation[c_ind] == (orders[c_ind] - 1):
                    carry[c_ind] = 1
        return variation, carry

    else:
        variation[ind] += 1
        if variation[ind] == (orders[ind] - 1):
            carry[ind] = 1
        return variation, carry

def variations(orders):
    variation = generate_default_state(orders)
    carry = generate_default_state(orders)

    #yield variation
    for number_variation in range(count_of_variations(orders)):
        for ind in range(len(variation)):
            if type(carry[ind]) == list:
                print('list')     
            #variation, carry = onestep(ind,carry, variation, orders)
            elif carry[ind] == 1:
                variation[ind] = 0
                carry[ind] = 0
                for c_ind in range(ind + 1, len(carry)):
                    if carry[c_ind] == 1:
                        variation[c_ind] = 0
                        carry[c_ind] = 0
                    else:
                        variation[c_ind] += 1
                        if variation[c_ind] == (orders[c_ind] - 1):
                            carry[c_ind] = 1
                        break
                yield variation, carry
                break

            else:
                variation[ind] += 1
                if variation[ind] == (orders[ind] - 1):
                    carry[ind] = 1
                yield variation, carry
                break

        #yield variation
            
            
            
            
            # if carry[ind] == 1:
            #     variation[ind] = 0
            #     carry[ind] = 0
            #     for c_ind in range(ind + 1, len(carry)):
            #         if carry[c_ind] == 1:
            #             variation[c_ind] = 0
            #             carry[c_ind] = 0
            #         else:
            #             variation[c_ind] += 1
            #             if variation[c_ind] == (orders[c_ind] - 1):
            #                 carry[c_ind] = 1
            #     yield variation

            # else:
            #     variation[ind] += 1
            #     if variation[ind] == (orders[ind] - 1):
            #         carry[ind] = 1
            #     yield variation
            #     break
                 

if __name__ == "__main__":
    #print(create_random_api_request(test_schema))
    #print(test_schema)
    data_types, keys = get_list_for_generator(test_schema)
    print(data_types)
    print(keys)
    orders = get_orders(data_types)
    print()
    for i, variation in enumerate(variations(orders)):
        variation, carry = variation
        print(str(i+1) + ': ' + variation.__str__() + ' carry:' +  carry.__str__() )


