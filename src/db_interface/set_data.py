from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

uri = getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

def create_area(name):
    sql = f"INSERT INTO areas (name) VALUES (:name);"
    db.session.execute(sql, {"name": name})
    db.session.commit()

def create_message(message, user, chain):
    if 0 < len(message) < 1000:        
        sql = f"INSERT INTO messages (content, user_id, chain_id)" \
                f" VALUES (:message, :user, :chain);"
        db.session.execute(sql, {"message": message, "user": user, "chain": chain})
        db.session.commit()
        return True
    return False

def create_msg_chain(header, user, area):
    if 0 < len(header) < 150:
        sql = f"INSERT INTO message_chains (header, user_id, area_id, visible)" \
                f" VALUES (:header, :user, :area, true);"
        db.session.execute(sql, {"header":header, "user":user, "area":area})
        db.session.commit()
        return True


def delete_msg_chain(id):
    sql = 'UPDATE message_chains SET visible=false WHERE id=:id'
    db.session.execute(sql, {'id': id})
    db.session.commit()


def delete_message(id):
    sql = 'UPDATE messages SET visible=false WHERE id=:id;'
    db.session.execute(sql, {'id': id})
    db.session.commit()


def edit_message(content, id):
    sql = 'UPDATE messages SET content=:content, time=NOW() WHERE id=:id;'
    db.session.execute(sql, {'content': content, 'id': id})
    db.session.commit()


def edit_chain(header, id):
    sql = 'UPDATE message_chains SET header=:header WHERE id=:id;'
    db.session.execute(sql, {'header': header, 'id': id})
    db.session.commit()



def delete_area(id):
    sql = "UPDATE areas SET visible=false WHERE id=:id;"
    db.session.execute(sql, {'id': id})
    db.session.commit()


def add_user(username, password, mod=False):
    sql = 'INSERT INTO users (username, password, moderator) VALUES (:username, :password, :moderator);'
    try:
        db.session.execute(sql, {'username': username, 'password': password, 'moderator': mod})
        db.session.commit()
        return True
    except:
        return False

