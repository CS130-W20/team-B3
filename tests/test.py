import requests
import json


def test_default():
    r = requests.get('http://localhost:8000/api/')
    if r.text != '"Welcome to the SwipeX API"':
        exit(1)


def main():
    test_default()


if __name__ == "__main__":
    main()
    exit(0)
