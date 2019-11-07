#!/usr/bin/python3

import spell
import os

from spell import app, db, bcrypt, file
from spell.userman import User

os.unlink(file)
pw_hash = bcrypt.generate_password_hash("Administrator@1").decode('utf-8')
#print (pw_hash)
#pw_hash = bcrypt.generate_password_hash("afdjlkfjakljfalkjadskljadslfjdsalk").decode('utf-8')
#print (pw_hash)
#print ( len(pw_hash))
db.create_all()

row = User()
row.username = "admin"
row.password = pw_hash
row.twofapassword = "12345678901"

db.session.add(row)
db.session.commit()
