import requests
import json
import sys
import os
import django

sys.path.insert(0, os.path.abspath('../backend'))  # noqa
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
from api.models import Account  # noqa


def test_account_create(res, expected, data):
    account = Account.objects.get(user_id=data['user_id'])
    if not account.is_valid():
        raise RuntimeError(f'Account could not be created: {data}')

    if response != expected_result:
        raise RuntimeError(f'Account creation did not return expected result {expected_result}')
