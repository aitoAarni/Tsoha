from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import src.db_interface.get_data as db_get
import src.tools.session as tools_session
import src.tools.user_inputs as tools_inputs
import os


uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        success = tools_inputs.create_area(request.values['area'], request.values['csrf_token'])
        if not success:
            return redirect(url_for('error', name='This area already exists'))
    areas = db_get.get_areas()
    return render_template('index.html', areas=areas, moderator=tools_session.is_mod(), session=tools_session.get_session())



@app.route('/area/<int:id>', methods=['POST', 'GET'])
def areas(id):
    if request.method == 'POST':
        success = tools_inputs.new_message_chain(request.form['header'], id, request.values['csrf_token'])
        if not success:
            return redirect(url_for('error', name='This chain already exists or too long name'))
    message_chains = tools_inputs.get_chains(id)
    return render_template(f'area.html', message_chains=message_chains, id=id, \
                             name=db_get.get_area_name(id), session=tools_session.get_session())


@app.route('/message_chain/<int:id>', methods=['POST', 'GET'])
def message_chain(id):
    if request.method == 'POST':

        success = tools_inputs.new_message(request.form["message"], id, request.values['csrf_token'])
        if not success:
            return redirect(url_for('error', name='message too long'))
    messages = tools_inputs.get_messages(id)
    previous = db_get.get_previous_area_id(id)
    print(previous)
    return render_template('message_chain.html', messages=messages, previous_page=previous, \
            id=id, header=db_get.get_chain_header(id), session=tools_session.get_session())


@app.route('/error/<name>')
def error(name):
    return render_template('error.html', error=name, session=tools_session.get_session())


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if len(request.form) > 0:
            username = request.form["username"]
            password = request.form["password"]
            successful_login = tools_session.log_in(username, password, request.values['csrf_token'])
            if not successful_login:
                return redirect(url_for('error', name='invalid login credentials'))
            return redirect(url_for("index"))
    return render_template('login.html', session=tools_session.get_session())

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and len(request.form) > 0:
        username = request.form["username"]
        password = request.form["password"]
        succesful_signing = tools_session.create_account(username, password, request.values['csrf_token'])
        if not succesful_signing:
            return redirect(url_for('error', name="Invalid username"))
        return redirect(url_for("index"))
    return render_template('register.html', session=tools_session.get_session())

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    tools_session.log_out(request.values['csrf_token'])
    return redirect(url_for('index'))
    
@app.route('/message_chain/<chain_id>/delete/<int:msg_id>')
def delete_message(chain_id, msg_id):
    tools_inputs.delete_message(msg_id)
    return redirect(url_for('message_chain', id=chain_id))

@app.route('/area/<area_id>/delete/<chain_id>')
def delete_chain(area_id, chain_id):
    tools_inputs.delete_msg_chain(chain_id)
    return redirect(url_for('areas', id=area_id))

@app.route("/delete/area/<id>")
def delete_area(id):
    if tools_inputs.delete_area(id):
        return redirect(url_for("index"))
    return redirect(url_for("error", name="Permission denied"))

@app.route('/message_chain/<chain_id>/edit/<msg_id>', methods=['GET', 'POST'])
def edit_message(chain_id, msg_id):
    message_data = db_get.get_a_message(msg_id)
    if request.method == 'POST':
        if not tools_inputs.edit_message(request.values['content'], msg_id, message_data['user_id'], request.values['csrf_token']):
            return redirect(url_for('error', name='Wrong user'))
        return redirect(url_for('message_chain', id=chain_id))
    return render_template('edit_msg.html', msg=message_data, session=tools_session.get_session())

@app.route('/area/<area_id>/edit/<chain_id>', methods=['GET', 'POST'])
def edit_chain(area_id, chain_id):
    chain_data = db_get.get_chain(chain_id)
    if request.method == 'POST':
        if not tools_inputs.edit_chain(request.values['header'], chain_id, chain_data['user_id'], request.values['csrf_token']):
            return redirect(url_for('error', name='Wrong user'))
        return redirect(url_for('areas', id=area_id))
    return render_template('edit_chain.html', msg=chain_data, session=tools_session.get_session())

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        messages = tools_inputs.search_for_messages(request.values['message'], request.values['csrf_token'])
    return render_template('search.html', search_word=request.values['message'], messages=messages, session=tools_session.get_session())