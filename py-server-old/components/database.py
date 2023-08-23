import json

filename = "data.json"

def load_data():
    try:
        with open(filename, "r") as f:
            if f.read() == "":
                return {}
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(filename, "w") as f:
        json.dump(data, f)