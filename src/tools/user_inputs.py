import src.db_interface.get_data as db_get
import src.db_interface.set_data as db_set 
from src.tools.session import csrf_token_wrong, session, user_id, is_mod

def create_area(name, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    try:
        db_set.create_area(name)
        return True
    except Exception:
        return False

def new_message(message, chain_id, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if len(message) > 1000:
        return False
    db_set.create_message(message, session['id'], chain_id)
    return True

def get_messages(chain):
    return db_get.get_messages(chain, user_id())
    
def delete_message(id):
    db_set.delete_message(id)


def get_chains(area):
    return db_get.get_msg_chains(area, user_id())

def new_message_chain(header, chain_id, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if len(header) > 100:
        return False
    db_set.create_msg_chain(header, session['id'], chain_id)
    return True

def delete_msg_chain(id):
    db_set.delete_msg_chain(id)

def edit_message(content, id, userid, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if user_id() == userid:
        db_set.edit_message(content, id)
        return True
    return False

def edit_chain(header, chain_id, userid, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    if user_id() == userid:
        db_set.edit_chain(header, chain_id)
        return True
    return False

def search_for_messages(word, csrf_token):
    if csrf_token_wrong(csrf_token):
        return False
    messages = db_get.search_for_messages(word, user_id())
    return messages

def delete_area(id):
    if is_mod():
        db_set.delete_area(id)
        return True
    return False