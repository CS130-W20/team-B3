# dictionary to define tests
from definitions import *


CASES = [
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
        'expected_results': {'STATUS': '0'},
        'func': test_account_create
    }
]
