import requests
import json


def post_uxixe(text):
    payload = {
        'content': text
    }

    r = requests.post('http://uxixe.com/api/new_gist', data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})

    return r.json()['html_url']


def post_gist(text):
    payload = {
        "description": "Jake Bot Output",
        "public": False,
        "files": {
            "output.txt": {
                "content": text
            }
        }
    }

    r = requests.post('https://api.github.com/gists', data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})
    print r.json()
    return r.json()['html_url']