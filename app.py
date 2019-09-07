import os

import requests

from flask_cors import CORS
from flask import Flask, request

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['POST'])
def send_email():
    result = requests.post(
        f"https://api.mailgun.net/v3/{os.environ['DOMAIN']}/messages",
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": request.form['email'],
              "to": [os.environ['EMAIL']],
              "subject": 'Message from ' + request.form['name'],
              "text": request.form['message']})

    return result
