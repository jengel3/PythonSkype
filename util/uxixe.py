import requests
import json


def post(text):
    payload = {
        'content': text
    }

    r = requests.post('http://uxixe.com/api/new_gist', data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})

    return r.json()['html_url']