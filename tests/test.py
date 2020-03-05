import requests
import json


def test_default():
    r = requests.get('https://localhost:8000/api')
    print(r.text)


def main():
    test_default()


if __name__ == "__main__":
    main()
