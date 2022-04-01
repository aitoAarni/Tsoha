from cgitb import text
from turtle import title
from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
db = SQLAlchemy(app)


@app.route("/")
def index():
    result = db.session.execute('SELECT content FROM messages')
    messages = result.fetchall()
    return render_template('index.html', count=len(messages), messages=messages)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/send', methods=['POST'])
def send():
    content = request.form['content']
    sql = 'INSERT INTO messages (content) VALUES (:content)'
    db.session.execute(sql, {'content':content})
    db.session.commit()
    return redirect('/')





@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    vastaus = str(eval(request.form["text"]))
    t = request.form["text"]

    return render_template("result.html", text=t, vastaus=vastaus)