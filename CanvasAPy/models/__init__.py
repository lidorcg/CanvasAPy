class Model:
    def __init__(self, json, api):
        self.api = api
        self.json = json

    def __getitem__(self, item):
        return self.json[item]

    def __setitem__(self, key, value):
        self.json[key] = value


class Course(Model):
    def save(self):
        pass
