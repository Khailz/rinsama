import json
from collections import OrderedDict
from pprint import pprint

with open('rooms.json') as data_file:
    data = json.load(data_file)

def getlast():
    v = max((int(v)) for v in data.keys())
    return v

while True:
    roomname = input('Room Name: ')
    roomdescrtiption = input('Description: ')
    lootlevel = input('lootlevel: ')
    room = {"{}".format(int(getlast()) + 1): {"name": "{}".format(roomname), "description": "{}".format(roomdescrtiption), "lootlevel": "{}".format(lootlevel), "directions": {}, "items": {}}}
    print(room)
    data.update(room)
    print(data)
    with open('rooms.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)