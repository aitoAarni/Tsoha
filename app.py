from cgitb import text
from turtle import title
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import src.database as database

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
db = SQLAlchemy(app)


@app.route("/")
def index():
    areas = database.get_areas()
    return render_template('index.html', areas=areas)



@app.route('/area/<int:id>')
def areas(id):
    message_chains = database.get_msg_chains(id)
    return render_template(f'area.html', message_chains=message_chains, id=id)

@app.route('/new_chain/<int:id>', methods=["POST"])
def new_area(id):
    header = request.form["header"]
    if database.check_if_value_exists('message_chains', 'header', header):
        return redirect(request.referrer)
    database.create_msg_chain(header, 1, id)    
    return redirect(request.referrer)

@app.route('/message_chain/<int:id>')
def message_chain(id):
    messages = database.get_messages(id)
    return render_template('message_chain.html', messages=messages, id=id)

@app.route('/new_message/<int:id>', methods=["POST"])
def new_message(id):
    message = request.form["message"]
    database.create_message(message, 1, id)
    return redirect(request.referrer)