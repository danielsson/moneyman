import sqlite3
from flask.ext.login import UserMixin
from flask import g
from app import app
from os import path

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    if not hasattr(g, "db"):
        g.db = connect_db()

    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
           for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = unicode(id)
        self.active = active

    def is_active(self):
        return self.active

    @staticmethod
    def byId(id):
        res = query_db("SELECT * FROM users WHERE id=? LIMIT 1;", [id], True)

        if res == None:
            return None

        return User(res['username'], res['id'])

    @staticmethod
    def byLogin(username, password):
        res = query_db("SELECT * FROM users WHERE username=? AND password=? LIMIT 1;", [username, password], True)

        if res == None:
            return None

        return User(res['username'], res['id'])



    def get_id(self):
        return self.id;

    def get_user_clf_path(self):
        return path.join(app.config['CLF_STORAGE'], str(self.id) + "_clf.pkl")