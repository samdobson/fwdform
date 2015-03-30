import os
from uuid import uuid4

from mandrill import Mandrill
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, abort

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
index_redirect_url = os.environ.get('INDEX_REDIRECT_URL') or \
                    'http://samdobson.github.io/fwdform'
mandrill_client = Mandrill(os.environ['MANDRILL_API_KEY'])
db = SQLAlchemy(app)

class User(db.Model):

    def __init__(self, email):
        self.email = email
        self.uuid = str(uuid4())

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    uuid = db.Column(db.String(36), unique=True)

@app.route('/')
def index():
    return redirect(index_redirect_url)

@app.route('/register', methods=['POST'])
def register():
    user = User.query.filter_by(email=request.form['email']).first()
    if user:
        return ('Email already registered', 403)
    user = User(request.form['email'])
    db.session.add(user)
    db.session.commit()
    return "Token: {}".format(user.uuid)

@app.route('/user/<uuid>', methods=['POST'])
def forward(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        return ('User not found', 406)
    message = {
               'to': [{'email': user.email}],
               'from_email': request.form['email'],
               'subject': 'Message from {}'.format(request.form['name']),
               'text': request.form['message'],
              }
    result = mandrill_client.messages.send(message=message)
    if result[0]['status'] != 'sent':
        abort(500)
    return 'Your message was sent successfully'

@app.errorhandler(400)
def bad_parameters(e):
    return ('<p>Missing information. Press the back button to complete '
            'the empty fields.</p><p><i>Developers: we were expecting '
            'the parameters "name", "email" and "message". You might '
            'also consider using JS validation.</i>', 400)

@app.errorhandler(500)
def error(e):
    return ('Sorry, something went wrong!', 500)

