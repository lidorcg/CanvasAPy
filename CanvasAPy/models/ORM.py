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
    def __init__(self, json, api):
        super().__init__(json, api)
        self.Modules = self.Modules(api, self)

    def update(self):
        url = 'courses/{}'.format(self['id'])
        data = {'course': self.json}
        return self.api.put(url, data)

    def delete(self):
        url = 'courses/{}'.format(self['id'])
        data = {'event': 'delete'}
        return self.api.delete(url, data)

    class Modules(API):
        def __init__(self, api, course):
            super().__init__(api)
            self.course = course

        def all(self):
            url = 'courses/{}/modules'.format(self.course['id'])
            modules = self.api.get_all(url)
            return [Module(mdl, self.api, self) for mdl in modules]

        def get(self, _id):
            url = 'courses/{}/modules/{}'.format(self.course['id'], _id)
            module = self.api.get(url).json()
            return Module(module, self.api, self)

        def new(self, name):
            url = 'courses/{}/modules '.format(self.course['id'])
            data = {' module': {'name': name}}
            module = self.api.post(url, data).json()
            return Module(module, self.api, self)

        def delete(self, _id):
            url = 'courses/{}/modules/{}'.format(self.course['id'], _id)
            return self.api.delete(url)


class Account(Model):
    def __init__(self, json, api):
        super().__init__(json, api)
        self.Courses = self.Courses(api, self)

    class Courses(API):
        def __init__(self, api, account):
            super().__init__(api)
            self.account = account

        def all(self):
            url = 'accounts/{}/courses'.format(self.account['id'])
            courses = self.api.get_all(url)
            return [Course(crs, self.api) for crs in courses]

        def get(self, _id):
            url = 'accounts/{}/courses/{}'.format(self.account['id'], _id)
            course = self.api.get(url).json()
            return Course(course, self.api)

        def new(self, name):
            url = 'accounts/{}/courses'.format(self.account['id'])
            data = {'account_id': self.account['id'], 'course': {'name': name}}
            course = self.api.post(url, data).json()
            return Course(course, self.api)


class Module(Model):
    def __init__(self, json, api, course):
        super().__init__(json, api)
        self.course = course

    def update(self):
        url = 'courses/{}/modules/{}'.format(self.course['id'], self['id'])
        data = {'module': self.json}
        return self.api.put(url, data)

    def delete(self):
        url = 'courses/{}/modules/{}'.format(self.course['id'], self['id'])
        return self.api.delete(url)
