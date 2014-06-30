import http


def post_uxixe(text):
    payload = {
        'content': text
    }

    json_data = http.post('http://uxixe.com/api/new_gist', payload, {"Content-Type": "application/json"})

    return json_data['html_url']


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

    json_data = http.post('https://api.github.com/gists', payload, headers={"Content-Type": "application/json"})
    return json_data['html_url']