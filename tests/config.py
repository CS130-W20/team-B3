from definitions import *

"""
Define Test Cases Here
{
    "name": give a name to your test
    "url": the endpoint, relative to http://localhost:8000/api/
    "type": GET or POST
    "data": data to POST
    "expected_result": data you need to verify the endpoint is functioning
    "func": function defined in definitions.py, takes type, expected_result, and data as parameters
}
"""

CASES = [
    {
        "name": "default",
        "url": '',
        "type": "GET",
        'data': {},
        "expected_result": '"Welcome to the SwipeX API"',
        "func": test_default
    },
    {
        "name": "sget",
        "url": 'swipes/sget/',
        "type": "GET",
        'data': {},
        "expected_result": {
                "halls_list": ["FEAST at Rieber", "De Neve", "Covel", "Bruin Plate"],
                "quick_list": ["Bruin Cafe", "Cafe 1919", "Rendezvous", "The Study at Hedrick"]
        },
        "func": test_sget
    },
    {
        "name": 'test_account_create',
        "url": 'accounts/create/',
        'type': 'POST',
        'data': {
            "loc": {
                "lat": 6,
                "lng": 7
            },
            "user_id": "test_name",
            "pp_email": "test_name@gmail.com",
            "pw": "password",
            "phone": "4242705206"
        },
        'expected_result': {'STATUS': '0'},
        'func': test_account_create
    },
    {
        "name": 'test_account_update',
        "url": 'accounts/update/',
        'type': 'POST',
        'data': {
            "user_id": "test_name",
            "pp_email": "test_name@gmail.com"
        },
        'expected_result': {'STATUS': '0'},
        'func': test_account_update
    }
]
