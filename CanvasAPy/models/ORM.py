class API:
    def __init__(self, api, model):
        self.api = api
        self.model = model
        self.url = None

    def all(self):
        objects = self.api.get_all(self.url.format(''))
        return [self.model(obj, self.api, self.url) for obj in objects]

    def get(self, _id):
        obj = self.api.get(self.url.format(_id)).json()
        return self.model(obj, self.api, self.url)

    def new(self, name):
        obj = self.api.post(self.url.format(''), self.new_data(name)).json()
        return self.model(obj, self.api, self.url)

    def delete(self, _id):
        return self.api.delete(self.url.format(_id))

    def new_data(self, name):
        pass


class Model:
    def __init__(self, json, api):
        self.api = api
        self.json = json
        self.url = None
        self.update_data = None
        self.delete_data = None

    def __str__(self):
        return '{}: {}'.format(self['id'], self['name'])

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.json[item]

    def __setitem__(self, key, value):
        self.json[key] = value

    def update(self):
        return self.api.put(self.url, self.update_data)

    def delete(self):
        return self.api.delete(self.url, self.delete_data)


class Account(Model):
    def __init__(self, json, api):
        super().__init__(json, api)
        self.url = 'accounts/{}'.format(self['id'])
        self.Courses = self.Courses(api, self.url, self['id'])

    class Courses(API):
        def __init__(self, api, url, account_id):
            super().__init__(api, Course)
            self.url = url + '/courses/{}'
            self.account_id = account_id

        def new_data(self, name):
            return {'account_id': self.account_id, 'course': {'name': name}}


class Course(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self.url = 'courses/{}'.format(self['id'])
        self.update_data = {'course': self.json}
        self.delete_data = {'event': 'delete'}
        self.Modules = self.Modules(api, self.url)

    class Modules(API):
        def __init__(self, api, url):
            super().__init__(api, Module)
            self.url = url + '/modules/{}'

        def new_data(self, name):
            return {'module': {'name': name}}


class Module(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self.url = url.format(self['id'])
        self.update_data = {'module': self.json}
