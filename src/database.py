from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import src.tools as tools

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL') # 'postgresql:///aare'
db = SQLAlchemy(app)

def create_area(name):
    try:
        db.session.execute(f"INSERT INTO areas (name) VALUES ('{name}');")
        return True
    except:
        return False


def get_areas():
    result = db.session.execute('SELECT * FROM areas;')
    areas = result.fetchall()
    return areas

def get_msg_chains(id):
    query = db.session.execute(f"SELECT header, id FROM message_chains WHERE area_id={id} and visible=true;")
    message_chains = query.fetchall()
    return message_chains

def create_msg_chain(header, user, area):
    if isinstance(area, str):
        area = db.session.execute(f"SELECT id FROM areas WHERE name='{area}';").fetchone()[0]
    if 0 < len(header) < 150:
        header = tools.character_escape(header)
        db.session.execute(f"INSERT INTO message_chains (header, user_id, area_id, visible)"
                        f" VALUES ('{header}', {user}, {area}, true);")
        db.session.commit()
        return True


def create_message(message, user, chain):
    now = datetime.now()
    time = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}"
    if isinstance(chain, str):
        chain = db.session.execute(f"SELECT id FROM message_chains WHERE header='{chain}';").fetchone()[0]
    if 0 < len(message) < 1000:        
        message = tools.character_escape(message)
        db.session.execute(f"INSERT INTO messages (content, user_id, chain_id, posting_date)"
                           f" VALUES ('{message}', {user}, {chain}, '{time}');")
        db.session.commit()
        return True
    return False

def get_messages(chain):
    if isinstance(chain, str):
        chain = db.session.execute(f"SELECT id FROM message_chains WHERE header='{chain}';").fetchone()[0]
    query = db.session.execute(f"SELECT content, posting_date FROM"
                                f" messages WHERE chain_id={chain} and visible=true;")
    messages = query.fetchall()
    return messages


def check_if_value_exists(table, column, value):
    query = db.session.execute(f"SELECT count(1)>0 FROM {table} WHERE {column}='{value}';")
    return query.fetchone()[0]
    

if __name__ == '__main__':
    create_message("I thinking that budhda ought to be the best", 1, 1)
