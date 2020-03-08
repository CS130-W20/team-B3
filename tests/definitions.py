import requests
import json

# Define test functions

def test_default():

    r = hit_endpoint("GET", 'http://localhost:8000/api/')

    if r.text != '"Welcome to the SwipeX API"':
        exit(1)

# test function get_swipes in backend/api/swipeviews.py
# check if its returning data for each dining hall
def test_sget():

    r = hit_endpoint("GET", 'http://localhost:8000/api/swipes/sget/')

    data = json.loads(r.json())

    halls_list = ["FEAST at Rieber", "De Neve", "Covel", "Bruin Plate"]
    quick_list = ["Bruin Cafe", "Cafe 1919", "Rendezvous", "The Study at Hedrick"]

    res_halls = []
    res_quick = []

    for h in data["halls"]:
        res_halls.append(h["name"])

    for q in data["quick"]:
        res_quick.append(q["name"])

    if set(res_halls) != set(halls_list):
        exit(1)

    if set(res_quick) != set(quick_list):
        exit(1)

def main():
    with open("tests.json", "w") as file:
        json.dump(data, file)
    test_default()
    test_sget()

if __name__ == "__main__":
    main()
    exit(0)
