import json
import os.path


class Config:
    data = {}

    def __init__(self):
        pass

    def reload(self):
        pass

    def load(self):
        if os.path.isfile('config.json'):
            self.data = json.load(open('config.json'))
        else:
            self.reset()

    def save(self):
        json.dump(self.data, open('config.json', 'w'), sort_keys=True, indent=4)

    def reset(self):
        json.dump(self.data, open('config.json', 'w'), sort_keys=True, indent=4)
        self.load()

    def get_value(self, key, default=None):
        return self.data[key] if key in self.data else default

    def set(self, key, value):
        new_key = {key: value}
        self.data.update(new_key)

    def set_default(self, key, value):
        if not key in self.data:
            self.set(key, value)
