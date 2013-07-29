from oauthlib.oauth2 import RequestValidator, LegacyApplicationServer
from flask import Flask, request, make_response, jsonify


app = Flask(__name__)


class Client(object):

    @property
    def client_id(self):
        return u'123'


class BasicValidator(RequestValidator):

    def authenticate_client(self, request, *args, **kwargs):
        request.client = Client()
        return True

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        return ['test']

    def save_bearer_token(self, token, request, *args, **kwargs):
        return 'http://blah/'

    def validate_bearer_token(self, token, scopes, request):
        return True

    def validate_grant_type(self, client_id, grant_type, client, request, *args, **kwargs):
        return True

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        return True

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        return True

    def validate_user(self, username, password, client, request, *args, **kwargs):
        return True

validator = BasicValidator()
server = LegacyApplicationServer(validator)


@app.route('/oauth2/token', methods=['POST'])
def access_token():
    print server.create_token_response(
        request.url,
        request.method,
        {
            'grant_type': 'password',
            'username': 'bob',
            'password': 'letmein!',
        },
        request.headers,
        {},
    )
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
