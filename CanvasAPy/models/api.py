from CanvasAPy.models import Course


class Courses:
    def __init__(self, api):
        self.api = api

    def all(self):
        courses = self.api.call('courses')
        return [Course(crs, self.api) for crs in courses]

    def get(self, _id):
        course = self.api.call('courses/{}'.format(_id))[0]
        return Course(course, self.api)

    def new(self, json):
        # ToDo call the api with the json needed and return the course from the response
        pass
