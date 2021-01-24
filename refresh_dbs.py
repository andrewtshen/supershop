from project import create_app, db
import glob, os

for f in glob.glob("P*.sqlite"):
    os.remove(f)

db.create_all(app=create_app(), bind=['user'])
