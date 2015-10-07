from .ORM import Account, Course


class API:
    def __init__(self, api):
        self.api = api


class Accounts(API):
    def all(self):
        accounts = self.api.get_all('accounts')
        return [Account(account, self.api) for account in accounts]

    def get(self, _id):
        account = self.api.get('accounts/{}'.format(_id)).json()
        return Account(account, self.api)


class Courses(API):
    def all(self):
        courses = self.api.get_all('courses')
        return [Course(crs, self.api) for crs in courses]

    def get(self, _id):
        course = self.api.get('courses/{}'.format(_id)).json()
        return Course(course, self.api)

    def delete(self, _id):
        data = {'event': 'delete'}
        return self.api.delete('courses/{}'.format(_id), data)
