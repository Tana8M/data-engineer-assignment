# from cerberus_list_schema import Validator
# from cerberus import Validator
from jsonschema import validate

'''
https://github.com/Fireclunge/cerberus-list-schema
https://towardsdatascience.com/do-not-use-if-else-for-validating-data-objects-in-python-anymore-17203e1d65fe
https://towardsdatascience.com/how-automated-data-validation-made-me-more-productive-7d6b396776
https://stackoverflow.com/questions/36757949/json-schema-definition-for-array-of-objects
'''


def json_validation_delisted_company(json: dict):
    '''

    :param json: dict
    :return: -
    '''
    schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'symbol': {'type': 'string'},
                'companyName': {'type': 'string'},
                'exchange': {'type': 'string'},
                'ipoDate': {'type': 'string'},
                'delistedDate': {'type': 'string'}
            },
            "required": [
                "symbol", 'companyName', 'exchange', 'ipoDate', 'delistedDate'
            ]
        }
    }
    try:
        validate(instance=json, schema=schema)
        print("Given JSON string is Valid")
    except ValueError as er:
        print(er)
        print("Given JSON string is InValid")
    return json


def json_validation_history_dividends(json: dict):
    '''

    :param json: dict
    :return:
    '''
    schema = {
        'type': 'object',
        'items': {
            'symbol': 'string',
            'historical': {'type': 'array'},
            'properties': {
                'date': {'type': 'string'},
                'label': {'type': 'string'},
                'adjDividend': {'type': 'number'},
                'dividend': {'type': 'number'},
                'recordDate': {'type': 'string'},
                'paymentDate': {'type': 'string'},
                'declarationDate': {'type': 'string'}
            }
        }
    }

    try:
        validate(instance=json, schema=schema)
        print("Given JSON string is Valid")
    except ValueError as er:
        print(er)
        print("Given JSON string is InValid")
    return json
