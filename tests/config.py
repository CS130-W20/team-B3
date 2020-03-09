from definitions import *

# define tests

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
    }
]
