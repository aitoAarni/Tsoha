import src.database as database
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def new_message(message, chain_id):
    if len(message) > 1000:
        return False
    database.create_message(message, session['id'], chain_id)
    return True

def new_message_chain(header, chain_id):
    if len(header) > 100:
        return False
    database.create_msg_chain(header, session['id'], chain_id)
    return True

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

def log_out():
    del session['id']
    del session['mod']