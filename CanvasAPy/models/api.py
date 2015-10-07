from CanvasAPy.models import Course


class Courses:
    def __init__(self, api):
        self.api = api

    def all(self):
        courses = self.api.get_all('courses')
        return [Course(crs, self.api) for crs in courses]

    def get(self, _id):
        course = self.api.get('courses/{}'.format(_id)).json()
        return Course(course, self.api)

    def new(self, name):
        params = {'course': {'name': name}}
        course = self.api.post('accounts/1/courses', params)
        # ToDo call the api with the json needed and return the course from the response
        return Course(course, self.api)
