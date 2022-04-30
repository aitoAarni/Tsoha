import secrets
import src.database as database
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def create_area(name, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    try:
        database.create_area(name)
        return True
    except Exception:
        return False

def new_message(message, chain_id, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
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

def new_message_chain(header, chain_id, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if len(header) > 100:
        return False
    database.create_msg_chain(header, session['id'], chain_id)
    return True

def delete_msg_chain(id):
    database.delete_msg_chain(id)

def log_in(name, password, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    user = database.username_exists(name)
    if not user:
        return False
    if check_password_hash(user.password, password):
        session['id'] = user.id
        session['mod'] = user.moderator
        session['logged'] = True
        return True
    return False

def create_account(name, password, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    pass_hash = generate_password_hash(password)
    result = database.add_user(name, pass_hash)
    if result:
        return log_in(name, password)
    return False



def is_mod():
    return session.get('mod', False)

def get_session():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    if 'logged' not in session:
        session['logged'] = False
    return session

def user_id():
    return session.get('id', 0)

def log_out(csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    del session['id']
    del session['mod']
    session['logged'] = False

def edit_message(content, id, userid, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if user_id() == userid:
        database.edit_message(content, id)
        return True
    return False

def edit_chain(header, chain_id, userid, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if user_id() == userid:
        database.edit_chain(header, chain_id)
        return True
    return False

def search_for_messages(word, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    messages = database.search_for_messages(word, user_id())
    return messages

def delete_area(id):
    if is_mod():
        database.delete_area(id)
        return True
    return False

def csrf_token_wrong(token):
    if token == session['csrf_token']:
        return False
    return True