import requests
import json
import urllib


PAID_URL = "https://minecraft.net/haspaid.jsp?user={}"

def verify(user, password):
    payload = {
        'agent': {'name': 'Minecraft', 'version': 1},
        'username': user,
        'password': password
    }

    r = requests.post('https://authserver.mojang.com/authenticate', data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})

    if 'error' in r.json():
        error = r.json()['errorMessage']
        if 'migrated' in error:
            return False, True
        return False, False
    else:
        return True, True


def has_paid(user):
    data = urllib.urlopen(PAID_URL.format(user)).read()
    return bool(data)
