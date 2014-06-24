import json


def save(conf):
    json.dump(conf, open('config.json', 'w'), sort_keys=True, indent=2)


def config():
    return json.load(open('config.json'))


