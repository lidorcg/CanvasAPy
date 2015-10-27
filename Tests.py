from CanvasAPy import OAuth
import CanvasAPy

print('Test API creation')
token = OAuth.get_token_from_file('token')
api = CanvasAPy.CanvasAPI('0.0.0.0:3000', token)

print('Test get_all for Accounts')
all_accounts = api.Accounts.all()
print('Test get single Account by id')
lid = api.Accounts.get(1)

print('Test REST for Courses')
print('create')
crs = lid.Courses.new({'name': 'Test_Course'})
print('read')
assert len(lid.Courses.all()) > 0
crs = lid.Courses.get(crs['id'])
print('update')
crs['name'] = 'Test_Course_new_name'
crs.update()
print('destroy')
crs.delete()

print('Test REST for Modules')
print('setup')
crs = lid.Courses.new({'name': 'Test_Course'})
print('create')
mdl = crs.Modules.new({'name': 'Test_Module'})
print('read')
assert len(crs.Modules.all()) > 0
mdl = crs.Modules.get(mdl['id'])
print('update')
mdl['name'] = 'Test_Module_new_name'
mdl.update()
print('destroy')
mdl.delete()

print('Test REST for Pages')
print('setup')
mdl = crs.Modules.new({'name': 'Test_Module'})
print('create')
pg = mdl.Pages.new({'title': 'Test_Page'})
print('read')
assert len(mdl.Pages.all()) > 0
pg = mdl.Pages.get(pg['id'])
print('update')
pg['title'] = 'Test_Page_new_name'
pg.update()
print('destroy')
pg.delete()

print('Test REST for Assignments')
print('create')
asn = mdl.Assignments.new({'name': 'Test_Assignment'})
print('read')
assert len(mdl.Assignments.all()) > 0
asn = mdl.Assignments.get(asn['id'])
print('update')
asn['name'] = 'Test_Assignment_new_name'
asn.update()
print('destroy')
asn.delete()

print('Test REST for Quizzes')
print('create')
qwz = mdl.Quizzes.new({'title': 'Test_Quiz'})
print('read')
assert len(mdl.Quizzes.all()) > 0
qwz = mdl.Quizzes.get(qwz['id'])
print('update')
qwz['name'] = 'Test_Quiz_new_name'
qwz.update()
print('destroy')
qwz.delete()

print('teardown')
mdl.delete()
crs.delete()

print('Done Testing!')
