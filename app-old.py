from flask import Flask
from flask.ext.oauthlib.provider import OAuth2Provider

app = Flask(__name__)
oauth = OAuth2Provider(app)


@oauth.clientgetter
def load_client(client_id):
    return None


@oauth.grantgetter
def load_grant(client_id, code):
    return None


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    return None


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    return None


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    return None


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    return None


@app.route('/oauth/token')
@oauth.token_handler
def access_token():
    return None


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
