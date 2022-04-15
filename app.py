from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import src.database as database
import src.tools as tools
import os


uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


@app.route("/")
def index():
    print(tools.logged_in())
    areas = database.get_areas()
    return render_template('index.html', areas=areas, logged=tools.logged_in())



@app.route('/area/<int:id>', methods=['POST', 'GET'])
def areas(id):
    if request.method == 'POST':
        success = tools.new_message_chain(request.form['header'], id)
        if not success:
            return redirect(url_for('error', name='This chain already exists or too long name'))
    message_chains = tools.get_chains(id)
    return render_template(f'area.html', message_chains=message_chains, id=id, logged=tools.logged_in())


@app.route('/message_chain/<int:id>', methods=['POST', 'GET'])
def message_chain(id):
    if request.method == 'POST':
        success = tools.new_message(request.form["message"], id)
        if not success:
            return redirect(url_for('error', name='message too long'))
    messages = tools.get_messages(id)
    return render_template('message_chain.html', messages=messages, id=id, logged=tools.logged_in())


@app.route('/error/<name>')
def error(name):
    return render_template('error.html', error=name, logged=tools.logged_in())


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if len(request.form) > 0:
            username = request.form["username"]
            password = request.form["password"]
            successful_login = tools.log_in(username, password)
            if not successful_login:
                return redirect(url_for('error', name='invalid login credentials'))
            return redirect(url_for("index"))
    return render_template('login.html', logged=tools.logged_in())

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and len(request.form) > 0:
        username = request.form["username"]
        password = request.form["password"]
        succesful_signing = tools.create_account(username, password)
        if not succesful_signing:
            return redirect(url_for('error', name="Invalid username"))
        return redirect(url_for("index"))
    return render_template('register.html', logged=tools.logged_in())

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    print('yeehaw')
    tools.log_out()
    return redirect(url_for('index'))
    