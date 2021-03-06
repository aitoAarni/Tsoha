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


def get_area_name(id):
    sql = 'SELECT name FROM areas WHERE id=:id;'
    query = db.session.execute(sql, {"id": id})
    name = query.fetchone()
    return name.name

def get_chain_header(id):
    sql = 'SELECT header FROM message_chains WHERE id=:id;'
    query = db.session.execute(sql, {'id': id})
    header = query.fetchone()
    return header.header

def search_for_messages(message, user_id):
    sql = "SELECT M.id, M.content, M.chain_id, to_char(M.time, 'DD-MM-YYYY HH24:MI') AS time, M.user_id=:user_id AS owned, "\
        "C.header, U.username FROM messages M, message_chains C, users U WHERE M.content LIKE :message AND M.chain_id=C.id"\
            " AND U.id=M.user_id ORDER BY M.time DESC;"
    query = db.session.execute(sql, {'message': f"%{message}%", 'user_id': user_id})
    messages = query.fetchall()
    return messages

def get_previous_area_id(chain_id):
    sql = "SELECT C.area_id, A.name FROM message_chains C, areas A WHERE C.id=:chain_id AND A.id=C.area_id;"
    query = db.session.execute(sql, {'chain_id': chain_id})
    area_id = query.fetchone()
    return area_id

def get_chain(id):
    sql = 'SELECT header, user_id FROM message_chains WHERE id=:id;'
    query = db.session.execute(sql, {'id': id})
    message = query.fetchone()
    return message


def username_exists(username):
    sql = 'SELECT password, id, moderator FROM users where username=:username;'
    query = db.session.execute(sql, {'username': username})
    user_info = query.fetchone()
    return user_info


def get_a_message(id):
    sql = 'SELECT content, user_id FROM messages WHERE id=:id;'
    query = db.session.execute(sql, {'id': id})
    message = query.fetchone()
    return message


def get_messages(chain, user_id):
    if isinstance(chain, str):
        chain = db.session.execute(f"SELECT id FROM message_chains WHERE header='{chain}';").fetchone()[0]
    sql = "SELECT M.id AS msg_id, M.content, to_char(M.time, 'DD-MM-YYYY HH24:MI') AS time, " \
            "U.username, U.id=:user_id AS owned FROM users U" \
            " LEFT JOIN messages M ON M.user_id=U.id WHERE M.chain_id=:chain and M.visible=true ORDER BY M.time DESC;"
    query = db.session.execute(sql, {"chain": chain, "user_id": user_id})
    messages = query.fetchall()
    return messages

def get_areas():
    sql = "SELECT A.name, A.id, COUNT(C.area_id) FILTER (WHERE C.visible) AS chain_count,"\
        " (SELECT COUNT(M.id) FROM messages M WHERE "\
        "M.chain_id IN (SELECT S.id FROM message_chains S WHERE S.area_id=A.id AND S.visible=true) "\
        "AND M.visible=true) AS msg_count, (SELECT MAX(to_char(time, 'DD-MM-YYYY HH24:MI')) FROM messages WHERE "\
        "chain_id IN (SELECT S.id FROM message_chains S WHERE S.area_id=A.id AND S.visible=true) "\
        "AND visible=true) AS time FROM areas A LEFT JOIN message_chains C ON A.id=C.area_id WHERE A.visible=true"\
        " GROUP BY A.id ORDER BY time DESC NULLS LAST;"
    result = db.session.execute(sql)
    areas = result.fetchall()
    return areas


def get_msg_chains(id, user_id):
    sql = "SELECT M.id, M.header, M.id, U.username, U.id=:user_id AS owned FROM users U " \
            "LEFT JOIN message_chains M ON M.user_id=U.id WHERE M.area_id=:id and M.visible=true;"
    query = db.session.execute(sql, {'id': id, "user_id": user_id})
    message_chains = query.fetchall()
    return message_chains
