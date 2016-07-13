import json
from wolframalpha import Client
import re


def log(login, string):
    with open("app.log", "a") as f:
        f.write(str((login, string)) + "\n")


def strToDict(string):
    return json.loads(string)


def dictToStr(dic):
    return str(json.dumps(dic, ensure_ascii=False))


def oneUserSelect(username, key, User):
    try:
        res = User.query.filter_by(username=username).first()
        return getattr(res, key)
    except:
        return False


def oneUserUpdate(username, value, User, db):
    try:
        res = User.query().filter_by(username=username).first()
        res.update(value)
        db.session.commit()
    except:
        return False


def insertUser(user, db):
    db.session.add(user)
    db.session.commit()


def checkUsername(string):
    pattern = re.compile('^[A-Za-z0-9_-]*$')
    return not (len(string) and pattern.match(string))


def wolframQuery(string):
    client = Client("R795LU-4EH4Q34378")
    res = client.query(string)
    return res.pods
