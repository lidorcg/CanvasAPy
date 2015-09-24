class Model:
    def __init__(self, json, api):
        self.api = api
        self.json = json

    def get(self, param):
        return self.json[param]


class Course(Model):
    def save(self):
        pass
