import src.database as database
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def create_area(name):
    try:
        database.create_area(name)
        return True
    except Exception:
        return False

def new_message(message, chain_id):
    if len(message) > 1000:
        return False
    database.create_message(message, session['id'], chain_id)
    return True

def get_messages(chain):
    return database.get_messages(chain, user_id())
    
def delete_message(id):
    database.delete_message(id)


def get_chains(area):
    return database.get_msg_chains(area, user_id())

def new_message_chain(header, chain_id):
    if len(header) > 100:
        return False
    database.create_msg_chain(header, session['id'], chain_id)
    return True

def delete_msg_chain(id):
    database.delete_msg_chain(id)

def log_in(name, password):
    user = database.username_exists(name)
    if not user:
        return False
    if check_password_hash(user.password, password):
        session['id'] = user.id
        session['mod'] = user.moderator
        return True
    return False

def create_account(name, password):
    pass_hash = generate_password_hash(password)
    result = database.add_user(name, pass_hash)
    if result:
        return log_in(name, password)
    return False



def is_mod():
    return session.get('mod', False)

def logged_in():
    if 'id' in session:
        return True
    return False

def user_id():
    return session.get('id', 0)

def log_out():
    del session['id']
    del session['mod']


def edit_message(content, id, userid):
    if user_id() == userid:
        database.edit_message(content, id)
        return True
    return False

def edit_chain(header, chain_id, userid):
    if user_id() == userid:
        database.edit_chain(header, chain_id)
        return True
    return False

def search_for_messages(word):
    messages = database.search_for_messages(word, user_id())
    return messages

def delete_area(id):
    if is_mod():
        database.delete_area(id)
        return True
    return False