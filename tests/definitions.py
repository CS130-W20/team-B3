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


def test_default(res, expected, data):
    """
    Test the default api endpoint

    Args:
        res: response object from GET request
        expected: "Welcome to the SwipeX API"
        data: not used

    Returns:
        n/a, raises error if test fails
    """

    if res.text != expected:
        raise RuntimeError(f'api/ endpoint did not return {expected}')


def test_sget(res, expected, data):
    """
    Test the sget endpoint, see if it is returning data for each dining hall

    Args:
        res: response object from GET request
        expected: Returns data for 4 dining halls and 4 quick service locations
        data: not used

    Returns:
        n/a, raises error if test fails
    """

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
    """
    Tests whether the account has successfully been created.

    Args:
        res (HTTP Reponse): The response from attempting to create the Account object.
        expected (Dict): The expected response
        data (Dict): The data used to create the object

    Raises:
        RuntimeError: If the account creation failed or if the expected response is different than the actual response.

    Returns:
        Account: The account object.
    """

    try:
        account = Account.objects.get(email=data['email'])
    except Account.DoesNotExist:
        raise RuntimeError(f'Failed to create account. {data}')

    if res.json()['STATUS'] != expected['STATUS']:
        account.delete()
        raise RuntimeError(f'Account creation did not return expected result {expected}')

    return account


def test_account_update(res, expected, data):
    """
    Tests account update endpoint.

    Args:
        res (HTTP Reponse): The response from attempting to create the Account object.
        expected (Dict): The expected response
        data (Dict): The data used to create the object

    Raises:
        RuntimeError: If the account update failed or if the expected response is different than the actual response.
    """

    try:
        account = Account.objects.get(email=data['email'])
        if float(account.cur_loc.lat) != data['loc']['lat'] or float(account.cur_loc.lng) != data['loc']['lng']:
            raise RuntimeError('Failed to update field within Account.')
    except Account.DoesNotExist:
        raise RuntimeError(f'Failed to update account because account does not exist. {data}')

    if dict(res.json()) != expected:
        raise RuntimeError(f'Account updating did not return expected result {expected}')
