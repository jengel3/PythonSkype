from urllib import urlopen
import requests


def get_url_data(url):
    return urlopen(url).read()


def post(url, payload, headers=None):
    r = requests.post(url=url, data=payload, headers=headers)
    return r.json()