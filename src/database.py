from email import message
from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

uri = getenv("DATABASE_URL")  # or other relevant config var
print(uri)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

def create_area(name):
    sql = f"INSERT INTO areas (name) VALUES (:name);"
    db.session.execute(sql, {"name": name})


def get_areas():
    result = db.session.execute('SELECT * FROM areas;')
    areas = result.fetchall()
    return areas

def get_msg_chains(id, user_id):
    sql = "SELECT M.header, M.id, U.username, U.id=:user_id AS owned FROM users U " \
            "LEFT JOIN message_chains M ON M.user_id=U.id WHERE M.area_id=:id and M.visible=true;"
    query = db.session.execute(sql, {'id': id, "user_id": user_id})
    message_chains = query.fetchall()
    print(user_id)
    print(message_chains)
    return message_chains

def create_msg_chain(header, user, area):
    if isinstance(area, str):
        area = db.session.execute(f"SELECT id FROM areas WHERE name='{area}' ;").fetchone()[0]
    if 0 < len(header) < 150:
        sql = f"INSERT INTO message_chains (header, user_id, area_id, visible)" \
                f" VALUES (:header, :user, :area, true);"
        db.session.execute(sql, {"header":header, "user":user, "area":area})
        db.session.commit()
        return True


def create_message(message, user, chain):
    if isinstance(chain, str):
        chain = db.session.execute(f"SELECT id FROM message_chains WHERE header='{chain}';").fetchone()[0]
    if 0 < len(message) < 1000:        
        sql = f"INSERT INTO messages (content, user_id, chain_id)" \
                f" VALUES (:message, :user, :chain);"
        db.session.execute(sql, {"message": message, "user": user, "chain": chain})
        db.session.commit()
        return True
    return False

def get_messages(chain, user_id):
    if isinstance(chain, str):
        chain = db.session.execute(f"SELECT id FROM message_chains WHERE header='{chain}';").fetchone()[0]
    sql = "SELECT M.content, to_char(M.time, 'DD-MM-YYYY HH24:MI'), " \
            "U.username, U.id=:user_id AS owned FROM users U" \
            " LEFT JOIN messages M ON M.user_id=U.id WHERE M.chain_id=:chain and M.visible=true ORDER BY M.time DESC;"
    query = db.session.execute(sql, {"chain": chain, "user_id": user_id})
    messages = query.fetchall()
    return messages

def username_exists(username):
    sql = 'SELECT password, id, moderator FROM users where username=:username'
    query = db.session.execute(sql, {'username': username})
    user_info = query.fetchone()
    return user_info

def add_user(username, password, mod=False):
    sql = 'INSERT INTO users (username, password, moderator) VALUES (:username, :password, :moderator)'
    try:
        db.session.execute(sql, {'username': username, 'password': password, 'moderator': mod})
        db.session.commit()
        return True
    except:
        print('error while trying to create an user')
        return False