from voluptuous import Schema
import random
from typing import Union
import typing
from types import GeneratorType
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

class NestedVariation:
    pass

def variations(orders):
    variation = generate_default_state(orders)
    carry = generate_default_carry_state(orders)
    variation_with_generator = generate_default_state(orders)
    #yield variation
    for number_variation in range(count_of_variations(orders)):
        for ind in range(len(variation)):
            if type(variation_with_generator[ind]) == list: #inicialization of generators in first iteration
                variation_with_generator[ind] = variations(orders[ind])

            elif carry[ind] == 1:
                variation[ind] = 0
                carry[ind] = 0
                for c_ind in range(ind + 1, len(carry)):
                    if carry[c_ind] == 1:
                        variation[c_ind] = 0
                        carry[c_ind] = 0
                    else:
                        if type(variation[c_ind]) == list:
                            for nv in variations(orders[c_ind]):
                                yield nv 
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
def make_generator(order):
    if type(order) == list:
        for i in variations(order):
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

def variations(orders):
    carry = generate_default_carry_state(orders)
    orders_1d = generate_1d_orders(orders)
    variation = []
    output = generate_default_state(orders)
    print(orders)
    for ind in range(len(orders)):
        variation.append(make_generator(orders[ind]))


    all_carry = False
    #while not all_carry:
    ## first iter
    for ind in range(len(variation)):
        output[ind] = next(variation[ind])
    yield output

    for number in range(count_of_variations(orders) - 1):
        for ind in range(len(variation)):
            if carry[ind] == 1:
                variation[ind] = make_generator(orders[ind])
                output[ind] = next(variation[ind])
                carry[ind] = 0
                for c_ind in range(ind + 1, len(carry)):
                    if carry[c_ind] == 1:
                        variation[c_ind] = make_generator(orders[ind])
                        output[c_ind] = next(variation[c_ind])
                        carry[c_ind] = 0
                    else:
                        output[c_ind] = next(variation[c_ind])

                        if output[c_ind] == (orders[c_ind] - 1):
                            carry[c_ind] = 1
                        break
                yield output
                break

            else:
                output[ind] = next(variation[ind])
                if output[ind] == (orders[ind] - 1):
                    carry[ind] = 1
                yield output
                break

        # all_carry = True
        # for c in carry:
        #     if c == 0:
        #         all_carry = False


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
    # for i, variation in enumerate(variations(orders)):
    #     variation, carry = variation
    #     print(str(i+1) + ': ' + variation.__str__() + ' carry:' +  carry.__str__() )
    for v in variations(orders):
        print(v)

