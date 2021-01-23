from project import create_app, db

db.create_all(app=create_app(), bind=['user', 'group', 'user_group'])
