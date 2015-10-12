class API:
    def __init__(self, api, url):
        self._api = api
        self._url = url
        self._model = lambda *x: None
        self._new_data = lambda x: None
        self._delete_data = None

    def all(self):
        objects = self._api.get_all(self._url.format(''))
        return [self._model(obj, self._api, self._url) for obj in objects]

    def get(self, pk):
        obj = self._api.get(self._url.format(pk)).json()
        return self._model(obj, self._api, self._url)

    def new(self, item):
        obj = self._api.post(self._url.format(''), self._new_data(item)).json()
        return self._model(obj, self._api, self._url)

    def delete(self, pk):
        return self._api.delete(self._url.format(pk), self._delete_data)


class Accounts(API):
    def __init__(self, api):
        super().__init__(api, '')
        self._model = Account
        self._url += '/accounts/{}'

    def new(self, item):
        raise Exception("You can't create new account from this API!")

    def delete(self, pk):
        raise Exception("You can't delete account from this API!")


class Courses(API):
    def __init__(self, api, url, account_id):
        super().__init__(api, url)
        self._url += '/courses/{}'
        self._model = Course
        self._new_data = lambda x: {'account_id': account_id, 'course': x}
        self._delete_data = {'event': 'delete'}

    def delete(self, pk):
        return self._api.delete('/courses/{}'.format(pk), self._delete_data)


class Modules(API):
    def __init__(self, api, url):
        super().__init__(api, url)
        self._url += '/modules/{}'
        self._model = Module
        self._new_data = lambda x: {'module': x}


class ModuleItems(API):
    def __init__(self, api, url):
        super().__init__(api, url)
        self._url += '/items/{}'
        self._model = ModuleItem
        self._new_data = lambda x: {'module_item': x}


class Pages(API):
    def __init__(self, api, url):
        super().__init__(api, url)
        self._url += '/pages/{}'
        self._model = Page
        self._new_data = lambda x: {'wiki_page': x}


class Assignments(API):
    def __init__(self, api, url):
        super().__init__(api, url)
        self._url += '/assignments/{}'
        self._model = Assignment
        self._new_data = lambda x: {'assignment': x}
        # ToDo check if work


class Quizzes(API):
    def __init__(self, api, url):
        super().__init__(api, url)
        self._url += '/quizzes/{}'
        self._model = Quiz
        self._new_data = lambda x: {' quiz': x}
        # ToDo check if work


class Model:
    def __init__(self, json, api):
        self._api = api
        self._json = json
        self._url = None
        self._update_data = None
        self._delete_data = None

    def __str__(self):
        return '{}: {}'.format(self['id'], self['name'])

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self._json[item]

    def __setitem__(self, key, value):
        self._json[key] = value

    def update(self):
        return self._api.put(self._url, self._update_data)

    def delete(self):
        return self._api.delete(self._url, self._delete_data)


class Account(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self.Courses = Courses(self._api, self._url, self['id'])


class Course(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self._url = '/courses/{}'.format(self['id'])
        self._update_data = {'course': self._json}
        self._delete_data = {'event': 'delete'}
        self.Modules = Modules(self._api, self._url)
        self.Pages = Pages(self._api, self._url)
        self.Assignments = Assignments(self._api, self._url)
        self.Quizzes = Quizzes(self._api, self._url)


class Module(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self._update_data = {'module': self._json}
        self.Items = ModuleItems(self._api, self._url)


class ModuleItem(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self._update_data = {'module_item': self._json}
        # ToDo check if work


class Page(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['url'])
        self._update_data = {'wiki_page': self._json}

    def __str__(self):
        return '{}: {}'.format(self['url'], self['title'])


class Assignment(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self._update_data = {'assignment': self._json}
        # ToDo check if work


class Quiz(Model):
    def __init__(self, json, api, url):
        super().__init__(json, api)
        self._url = url.format(self['id'])
        self._update_data = {'quiz': self._json}
        # ToDo check if work
