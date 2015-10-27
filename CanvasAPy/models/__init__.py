class API:
    def __init__(self, api, url, parent):
        self._api = api
        self._url = url
        self._parent = parent
        self._model = lambda *x: None
        self._new_data = lambda x: None
        self._delete_data = None

    def all(self):
        objects = self._api.get_all(self._url.format(''))
        return [self._model(obj, self._api, self._url, self._parent) for obj in objects]

    def get(self, pk):
        obj = self._api.get(self._url.format(pk)).json()
        return self._model(obj, self._api, self._url, self._parent)

    def new(self, item):
        obj = self._api.post(self._url.format(''), self._new_data(item)).json()
        return self._model(obj, self._api, self._url, self._parent)

    def delete(self, pk):
        return self._api.delete(self._url.format(pk), self._delete_data)


class Accounts(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._model = Account
        self._url += '/accounts/{}'

    def new(self, item):
        raise Exception("You can't create new account from this API!")

    def delete(self, pk):
        raise Exception("You can't delete account from this API!")


class Courses(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/courses/{}'
        self._model = Course
        self._new_data = lambda x: {'account_id': self._parent['id'], 'course': x}
        self._delete_data = {'event': 'delete'}

    def delete(self, pk):
        return self._api.delete('/courses/{}'.format(pk), self._delete_data)


class Modules(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/modules/{}'
        self._model = Module
        self._new_data = lambda x: {'module': x}


class ModuleItems(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/items/{}'
        self._model = ModuleItem
        self._new_data = lambda x: {'module_item': x}


class Pages(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/pages/{}'
        self._model = Page
        self._new_data = lambda x: {'wiki_page': x}


class ModulePages:
    def __init__(self, course_pages, module_items):
        self._course_pages = course_pages
        self._module_items = module_items

    def all(self):
        items = self._module_items.all()
        return [itm for itm in items if itm['type'] == 'Page']

    def get(self, pk):
        itm = self._module_items.get(pk)
        if itm['type'] == 'Page':
            return itm

    def new(self, item):
        crs_pg = self._course_pages.new(item)
        mdl_itm = self._module_items.new({'type': 'Page', 'page_url': crs_pg['url']})
        return mdl_itm

    def delete(self, pk):
        return self._module_items.delete(pk)


class Assignments(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/assignments/{}'
        self._model = Assignment
        self._new_data = lambda x: {'assignment': x}


class ModuleAssignments:
    def __init__(self, course_assignments, module_items):
        self._course_assignments = course_assignments
        self._module_items = module_items

    def all(self):
        items = self._module_items.all()
        return [itm for itm in items if itm['type'] == 'Assignment']

    def get(self, pk):
        itm = self._module_items.get(pk)
        if itm['type'] == 'Assignment':
            return itm

    def new(self, item):
        crs_tsk = self._course_assignments.new(item)
        mdl_itm = self._module_items.new({'type': 'Assignment', 'content_id': crs_tsk['id']})
        return mdl_itm

    def delete(self, pk):
        return self._module_items.delete(pk)


class Quizzes(API):
    def __init__(self, api, url, parent):
        super().__init__(api, url, parent)
        self._url += '/quizzes/{}'
        self._model = Quiz
        self._new_data = lambda x: {'quiz': x}


class ModuleQuizzes:
    def __init__(self, course_quizzes, module_items):
        self._course_quizzes = course_quizzes
        self._module_items = module_items

    def all(self):
        items = self._module_items.all()
        return [itm for itm in items if itm['type'] == 'Quiz']

    def get(self, pk):
        itm = self._module_items.get(pk)
        if itm['type'] == 'Quiz':
            return itm

    def new(self, item):
        crs_qwz = self._course_quizzes.new(item)
        mdl_itm = self._module_items.new({'type': 'Quiz', 'content_id': crs_qwz['id']})
        return mdl_itm

    def delete(self, pk):
        return self._module_items.delete(pk)


class Model:
    def __init__(self, json, api, parent):
        self._json = json
        self._api = api
        self._parent = parent
        self._url = lambda: None
        self._update_data = lambda: None
        self._delete_data = lambda: None

    def __str__(self):
        return '{}: {}'.format(self['id'], self['name'])

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self._json[item]

    def __setitem__(self, key, value):
        self._json[key] = value

    def update(self):
        response = self._api.put(self._url(), self._update_data())
        self._json = response.json()
        return response

    def delete(self):
        return self._api.delete(self._url(), self._delete_data())


class Account(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['id'])
        self.Courses = Courses(self._api, self._url(), self)


class Course(Model):
    def __init__(self, json, api, _, parent):
        super().__init__(json, api, parent)
        self._url = lambda: '/courses/{}'.format(self['id'])
        self._update_data = lambda: {'course': self._json}
        self._delete_data = lambda: {'event': 'delete'}
        self.Modules = Modules(self._api, self._url(), self)
        self.Pages = Pages(self._api, self._url(), self)
        self.Assignments = Assignments(self._api, self._url(), self)
        self.Quizzes = Quizzes(self._api, self._url(), self)


class Module(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['id'])
        self._update_data = lambda: {'module': self._json}
        self.Items = ModuleItems(self._api, self._url(), self)
        self.Pages = ModulePages(parent.Pages, self.Items)
        self.Assignments = ModuleAssignments(parent.Assignments, self.Items)
        self.Quizzes = ModuleQuizzes(parent.Quizzes, self.Items)


class ModuleItem(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['id'])
        self._update_data = lambda: {'module_item': self._json}

    def __str__(self):
        return '{}: {}'.format(self['type'], self['title'])


class Page(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['url'])
        self._update_data = lambda: {'wiki_page': self._json}

    def __str__(self):
        return '{}: {}'.format(self['url'], self['title'])


class Assignment(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['id'])
        self._update_data = lambda: {'assignment': self._json}


class Quiz(Model):
    def __init__(self, json, api, url, parent):
        super().__init__(json, api, parent)
        self._url = lambda: url.format(self['id'])
        self._update_data = lambda: {'quiz': self._json}
