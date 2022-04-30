import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import src.db_interface.set_data as db_set
import src.db_interface.get_data as db_get


def log_in(name, password, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    user = db_get.username_exists(name)
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
    result = db_set.add_user(name, pass_hash)
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

def csrf_token_wrong(token):
    if token == session['csrf_token']:
        return False
    return True