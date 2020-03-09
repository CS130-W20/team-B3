import requests
import json
import sys
import os
import django

# Define test functions for each endpoint

sys.path.insert(0, os.path.abspath('../backend'))  # noqa
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from api.models import Account  # noqa

# Test the default api endpoint
def test_default(res, expected, data):

    if res.text != expected:
        raise RuntimeError(f'api/ endpoint did not return {expected}')

# test function get_swipes in backend/api/swipeviews.py
# check if its returning data for each dining hall

def test_sget(res, expected, data):

    r = json.loads(res.json())

    res_halls = []
    res_quick = []

    for h in r["halls"]:
        res_halls.append(h["name"])

    for q in r["quick"]:
        res_quick.append(q["name"])

    if set(res_halls) != set(expected["halls_list"]):
        raise RuntimeError(f'sget/ endpoint did not return all dining halls, returned {expected["halls_list"]}')

    if set(res_quick) != set(expected["quick_list"]):
        raise RuntimeError(f'sget/ endpoint did not return all quickservice, returned {expected["quick_list"]}')
