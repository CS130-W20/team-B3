import requests
import json
import sys
import os
import django

# Define test functions for each endpoint

sys.path.insert(0, os.path.abspath('../backend'))  # noqa
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from api.models import Account, Bid  # noqa


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
        expected (Dict): The expected response.
        data (Dict): The data used to issue the test.

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
        res (HTTP Reponse): The response from attempting to update the Account object.
        expected (Dict): The expected response.
        data (Dict): TThe data used to issue the test.

    Raises:
        RuntimeError: If the account update failed or if the expected response is different than the actual response.
    """

    try:
        account = Account.objects.get(email=data['email'])
        if float(account.cur_loc.lat) != data['loc']['lat'] or float(account.cur_loc.lng) != data['loc']['lng']:
            raise RuntimeError('Failed to update field within Account.')
    except Account.DoesNotExist:
        raise RuntimeError(f'Failed to update account because account does not exist. {data}')

    if res.json()['STATUS'] != expected['STATUS']:
        raise RuntimeError(f'Account updating did not return expected result {expected}')


def test_account_checkexistence(res, expected, data):
    """
    Tests the account_checkexistence endpoint at url accounts/check/

    Args:
        res (HTTP Reponse): The response from attempting to check for existence.
        expected (Dict): The expected response
        data (Dict): The data used to issue the test.

    Raises:
        RuntimeError: If the account check failed or if the expected response is different than the actual response.
    """

    try:
        account = Account.objects.get(email=data['email'])
    except Account.DoesNotExist:
        raise RuntimeError(f'Account does not exist.')

    res_json = dict(res.json())

    if res_json['exists'] != expected['exists'] or res_json['STATUS'] != expected['STATUS']:
        raise RuntimeError(f'Account checking did not return expected result {expected}')


def test_bid_placebid(res, expected, data):
    """
    Tests the place bid endpoint at url buying/buy/.

    Args:
        res (HTTP Reponse): The response from attempting to place a Bid.
        expected (Dict): The expected response.
        data (Dict): The data used to issue the test.

    Raises:
        RuntimeError: If the bid creation failed or if the expected response is different than the actual response.

    Returns:
        Bid: The Bid object.
    """
    try:
        bid = Bid.objects.get(buyer_id=data['user_id'], hall_id=data['hall_id'])
    except Bid.DoesNotExist:
        raise RuntimeError(f'Bid was not created.')

    res_json = dict(res.json())
    if res_json['STATUS'] != expected['STATUS'] or res_json['REASON'] != expected['REASON']:
        bid.delete()
        raise RuntimeError(f'Bid creation did not return expected result {expected}')

    return bid


def test_get_best_pairing(res, expected, data):
    """
    Tests the get_best_pairing endpoint at url selling/get_bid/.

    Args:
        res (HTTP Reponse): The response from attempting to match the Bid.
        expected (Dict): The expected response.
        data (Dict): The data used to issue the test.

    Raises:
        RuntimeError: If the bid matching fails to return the expected Bid.
    """

    res_json = res.json()
    if res_json['buyer'] != expected['buyer'] or res_json['hall_id'] != expected['hall_id']:
        raise RuntimeError(f'get_best_pairing did not return the expected best pairing .')

def test_timeinterval_info(res, expected, data):
    """
    Tests the timeinterval_info endpoint at url swipes/timeinterval_info/.

    Args:
        res (HTTP Reponse): The response from the server.
        expected (Dict): The expected response.
        data (Dict): The data used to issue the test.

    Raises:
        RuntimeError: when the reponse data is empty
    """

    res_json = res.json()
    if not res_json:
        raise RuntimeError(f'The timeinterval_info endpoint return bad value' )

def test_get_swipe(res, expected, data):
    """
    Tests the get_swipe endpoint at url buying/get_swipe/.

    Args:
        res (HTTP Reponse): The response from the server.
        expected (Dict): The expected response.
        data (Dict): The data used to issue the test.

    Raises:
        RuntimeError: when the reponse data is empty
    """

    res_json = res.json()
    if not res_json:
        raise RuntimeError(f'The get_swipe endpoint return bad value' )