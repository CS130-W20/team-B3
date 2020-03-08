import config

api_endpoint = 'http://localhost:8000/api/'

# hit an endpoint
def hit_endpoint(type, api, payload = {}):

    res = {}

    if type == "GET":
        res = requests.get(api)
    elif type == "POST":
        res = requests.post(api, json=payload)
    else:
        exit(1)

    if res.status_code != 200:
        exit(1)

    return res

def main():

    for test in config:
        print(test["name"])

        res = hit_endpoint(test["type"], api_endpoint + test["url"])
        test["func"](res, test["expected_result"])

if __name__ == "__main__":
    main()
