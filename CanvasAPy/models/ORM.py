class API:
    def __init__(self, api):
        self.api = api


class Model:
    def __init__(self, json, api):
        self.api = api
        self.json = json

    def __str__(self):
        return '{}: {}'.format(self['id'], self['name'])

    def __getitem__(self, item):
        return self.json[item]

    def __setitem__(self, key, value):
        self.json[key] = value


class Course(Model):
    def update(self):
        data = {'course': self.json}
        return self.api.put('courses/{}'.format(self['id']), data)

    def delete(self):
        data = {'event': 'delete'}
        return self.api.delete('courses/{}'.format(self['id']), data)


class Account(Model):
    def __init__(self, json, api):
        super().__init__(json, api)
        self.Courses = self.Courses(api, self)

    class Courses(API):
        def __init__(self, api, account):
            super().__init__(api)
            self.account = account

        def all(self):
            courses = self.api.get_all('accounts/{}/courses'.format(self.account['id']))
            return [Course(crs, self.api) for crs in courses]

        def get(self, _id):
            course = self.api.get('accounts/{}/courses/{}'.format(self.account['id'], _id)).json()
            return Course(course, self.api)

        def new(self, name):
            url = 'accounts/{}/courses'.format(self.account['id'])
            data = {'account_id': self.account['id'], 'course': {'name': name}}
            course = self.api.post(url, data).json()
            return Course(course, self.api)
