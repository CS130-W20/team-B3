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
        "url": 'swipes/homescreen_info/',
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
            'status': '0',
            'name': 'test_name',
            'phone': '12345678',
            'email': 'test_email@email.com',
            'loc': {
                'lat': 1.0,
                'lng': 1.0
            }
        },
        'expected_result': {'STATUS': '0'},
        'func': test_account_create
    },
    {
        "name": 'test_account_update',
        "url": 'accounts/update/',
        'type': 'POST',
        'data': {
            "name": "test_name",
            "email": "test_email@email.com",
            'loc': {
                'lat': 2.0,
                'lng': 2.0
            }
        },
        'expected_result': {'STATUS': '0'},
        'func': test_account_update
    },
    {
        'name': 'test_account_checkexistence',
        'url': 'accounts/check/',
        'type': 'POST',
        'data': {
            'name': 'test_name',
            'email': 'test_email@email.com',
            'loc': {
                'lat': 2.0,
                'lng': 2.0
            }
        },
        'expected_result': {'exists': '1', 'STATUS': '0'},
        'func': test_account_checkexistence
    },
    {
        'name': 'test_bid_placebid',
        'url': 'buying/buy/',
        'type': 'POST',
        'data': {
            'user_id': 1,
            'hall_id': 1,
            'desired_price': 7.00,
            'time_intervals': [{
                'start': '15:00',
                'end': '16:00'
            }]
        },
        'expected_result': {'STATUS': '0', 'REASON': 'SWIPE/BID CREATED, NO ELIGIBLE COMPLEMENT PAIRED'},
        'func': test_bid_placebid
    },
    {
        'name': 'test_get_best_pairing',
        'url': 'selling/get_bid/',
        'type': 'POST',
        'data': {
            'hall_id': 1,
            'time_intervals': [{
                'start': '15:00',
                'end': '16:00'
            }],
            'desired_price': 7.00
        },
        'expected_result': {'buyer': 1, 'hall_id': 1},
        'func': test_get_best_pairing
    }
]
