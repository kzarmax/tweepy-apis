import json


# Read user data from json file
def read_data():
    with open("user.json") as openfile:
        json_object = json.load(openfile)

    print(json_object)
    return json_object


def write_data(user_data):
    # Serializing json
    json_object = json.dumps(user_data, indent=4)

    with open("user.json", "w") as outfile:
        outfile.write(json_object)
