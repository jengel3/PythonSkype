from urllib import urlopen
import requests
import json


def get_url_data(url):
    return urlopen(url).read()


def post(url, payload, headers=None):
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    return r.json()