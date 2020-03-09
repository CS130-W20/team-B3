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
                "halls_list" : ["FEAST at Rieber", "De Neve", "Covel", "Bruin Plate"],
                "quick_list" : ["Bruin Cafe", "Cafe 1919", "Rendezvous", "The Study at Hedrick"]
        },
        "func": test_sget
    },
]
