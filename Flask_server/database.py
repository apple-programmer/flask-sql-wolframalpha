from flask_sqlalchemy import SQLAlchemy
from Flask_server import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    data = db.Column(db.String)

    def __init__(self, *args):
        self.username, self.password, self.data = args


if __name__ == "__main__":
    db.create_all()
