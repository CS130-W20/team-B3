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

def test_account_create(res, expected, data):
    account = Account.objects.get(user_id=data['user_id'])
    if not account.is_valid():
        raise RuntimeError(f'Account could not be created: {data}')


def test_account_create(res, expected, data):
    """
    Tests whether the account has successfully been created.

    Args:
        res (HTTP Reponse): The response from attempting to create the Account object.
        expected (Dict): The expected response
        data (Dict): The data used to create the object

    Raises:
        RuntimeError: If the account creation failed or if the expected response is different than the actual response.
        RuntimeError: [description]

    Returns:
        Account: The account object.
    """

    try:
        account = Account.objects.get(user_id=data['user_id'])
    except Account.DoesNotExist:
        raise RuntimeError(f'Failed to create account. {data}')

    if dict(res.json()) != str(expected):
        return account
        raise RuntimeError(f'Account creation did not return expected result {expected}')

    return account
