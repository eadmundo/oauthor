import os
from requests_oauthlib import OAuth2Session
from flask import Flask, session, redirect, request, url_for, jsonify, render_template
from flask.ext.login import (
    LoginManager, current_user, login_user,
    logout_user, UserMixin
)
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

provider_base_url = 'http://localhost:5002'

client_id = os.environ.get('GITHUB_CONSUMER_KEY')
client_secret = os.environ.get('GITHUB_CONSUMER_SECRET')

authorization_base_url = '{}/login/oauth/authorize'.format(provider_base_url)
token_url = '{}/login/oauth/access_token'.format(provider_base_url)


@app.route('/login/')
def login():
    github = OAuth2Session(client_id, scope=['repo'])
    authorization_url, state = github.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/callback/')
def authorise():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
        authorization_response=request.url)
    session['oauth_token'] = token
    # user_json = github.get('https://api.github.com/user').json()
    user_json = {'login': 'eadmundo'}
    username = user_json['login']
    # user = db.session.query(Users).filter_by(username=username).first()
    user = Users(username)
    if user is None:
        user = Users(username)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('.profile'))


@app.route('/')
def index():
    if current_user.is_authenticated():
        github = OAuth2Session(client_id, token=session['oauth_token'])
        r = github.get(
            'https://api.github.com/repos/{}/searchology/events'.format(
                current_user.username), headers={
                    'If-None-Match': session.get('etag', None)
                })
        if r.status_code == 200:
            session['etag'] = r.headers['etag']
            for event in r.json():
                print event['type'], event['created_at']
        print r.status_code
    return render_template('index.jinja')


@app.route('/logout/')
def logout():
    session.pop('oauth_token', None)
    session.pop('oauth_state', None)
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/')
def profile():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).filter_by(id=int(user_id)).first()


@app.context_processor
def current_user_context():
    return dict(current_user=current_user)


if __name__ == '__main__':
    app.run(port=5001)
