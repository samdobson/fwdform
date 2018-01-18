import os
from uuid import uuid4
import logging

from mandrill import Mandrill
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, abort


from backends import backends

logger = logging.getLogger(__name__)
app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

logging.basicConfig(level='WARNING' if not os.environ.get('FWDFORM_DEBUG', False) else 'DEBUG')

try:
    backend_name = os.environ['FWDFORM_BACKEND']
except KeyError:
    raise Exception('environment variable FWDFORM_BACKEND has to be set (allowed values: {})'.format(", ".join(backends)))
if backend_name not in backends:
    raise Exception('Unknown value for FWDFORM_BACKEND: {} (allowed: {})'.format(backend_name, ", ".join(backends)))

backend = backends[backend_name]()

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
    return redirect('http://samdobson.github.io/fwdform')

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

    send_ok = backend.send_message(to=user.email, 
                                   from_email=request.form['email'], 
                                   subject='Message from {}'.format(request.form['name']),
                                   text=request.form['message'])
    if not send_ok:
        abort(500)
    if 'next' in request.form:
        return redirect(request.form['next'])
    return 'Your message was sent successfully'

@app.errorhandler(400)
def bad_parameters(e):
    return ('<p>Missing information. Press the back button to complete '
            'the empty fields.</p><p><i>Developers: we were expecting '
            'the parameters "name", "email" and "message". You might '
            'also consider using JS validation.</i>', 400)

@app.errorhandler(500)
def error(e):
    logger.error(e)
    return ('Sorry, something went wrong!', 500)

