from app import db, User
import json

dat = {'name' : 'Admin Name', 'ip' : '192.168.192.140'}

admin = User('admin', 'passs', str(json.dumps(dat, ensure_ascii=False)))

dat = {'name' : 'Roman Nikitin', 'ip' : '192.168.192.140'}
roman = User('roman', "123456780987654321", str(json.dumps(dat, ensure_ascii=False)))

db.session.add(admin)
db.session.add(roman)
db.session.commit()