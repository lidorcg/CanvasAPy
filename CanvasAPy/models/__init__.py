class API:
    def __init__(self, api):
        self.api = api
        self.url = None
        self.model = lambda *x: None
        self.new_data = lambda x: None

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


class Accounts(API):
    def __init__(self, api):
        super().__init__(api)
        self.model = Account
        self.url = '/accounts/{}'

    def new(self, name):
        raise Exception("You can't create new account from this API!")

    def delete(self, _id):
        raise Exception("You can't delete account from this API!")


class Courses(API):
    def __init__(self, api, url, account_id):
        super().__init__(api)
        self.url = url + '/courses/{}'
        self.model = Course
        self.new_data = lambda x: {'account_id': account_id, 'course': {'name': x}}


class Modules(API):
    def __init__(self, api, url):
        super().__init__(api)
        self.url = url + '/modules/{}'
        self.model = Module
        self.new_data = lambda x: {'module': {'name': x}}


class Model:
    def __init__(self, json, api, url):
        self.api = api
        self.json = json
        self.url = url.format(self['id'])
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
    def __init__(self, json, api, url):
        super().__init__(json, api, url)
        self.Courses = Courses(api, self.url, self['id'])


class Course(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api, url)
        self.url = '/courses/{}'.format(self['id'])
        self.update_data = {'course': self.json}
        self.delete_data = {'event': 'delete'}
        self.Modules = Modules(api, self.url)


class Module(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api, url)
        self.update_data = {'module': self.json}
