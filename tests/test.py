from config import CASES
import requests

api_endpoint = 'http://localhost:8000/api/'

# hit an endpoint


def hit_endpoint(type, api, payload={}):

    res = {}

    if type == "GET":
        res = requests.get(api)
    elif type == "POST":
        res = requests.post(api, json=payload)
    else:
        raise RuntimeError(f'Call to {api} did not use GET or POST')

    if res.status_code != 200:
        raise RuntimeError(f'{api} returned {res.status_code}')

    return res


def delete_test_data(test_data):
    for obj in test_data:
        if obj is not None:
            obj.delete()


def main():

    count = 0
    test_data = []
    for test in CASES:
        try:
            print(f'Testing {test["name"]}...', end='')
            res = hit_endpoint(test["type"], api_endpoint + test["url"], test['data'])
            test_data.append(test["func"](res, test["expected_result"], test['data']))
        except RuntimeError as err:
            print(f'failed: {err}')
            count += 1
            continue
        else:
            print('passed')

    delete_test_data(test_data)
    if count != 0:
        print(f'{count} tests failed.')
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
