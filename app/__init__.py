import os
import sys
# Injects our external libraries from the libs directory into our system path.
# This way we can use them on gae!
sys.path.insert(0, 'libs')

from flask import Flask
from google.appengine.ext.webapp.util import run_wsgi_app
from app import views

app = Flask(__name__)

# Register the blueprint from views.py so that our app knows how to route requests.
app.register_blueprint(views.blueprint)

# This key used for encrypting user sessions.
# http://flask.pocoo.org/docs/quickstart/#sessions
SECRET_KEY = 'i am a secret key for encrypting user sessions into their cookies'
app.secret_key = SECRET_KEY


if __name__ == '__main__':
    run_wsgi_app(app)