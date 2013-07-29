from oauthlib.oauth1 import RequestValidator, WebApplicationServer
from flask import Flask, request, Response
import time


import logging
import sys
log = logging.getLogger('oauthlib')
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)


app = Flask(__name__)


class BasicValidator(RequestValidator):

    @property
    def dummy_client(self):
        return None

    @property
    def dummy_request_token(self):
        return None

    @property
    def enforce_ssl(self):
        return False

    def get_client_secret(self, client_key, request):
        return u'thing'

    def get_request_token_secret(self, client_key, token, request):
        return u'other-thing'

    def get_rsa_key(self, client_key, request):
        return u'an-rsa-public-key'

    def save_access_token(self, token, request):
        pass

    def validate_client_key(self, client_key, request):
        return True

    def validate_request_token(self, client_key, token, request):
        return True

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        return True

    def validate_verifier(self, client_key, token, verifier, request):
        return True

    def get_realms(self, token, request):
        return ['default', 'special']


validator = BasicValidator()

server = WebApplicationServer(validator)


# @app.route('/oauth1/token', methods=['POST'])
# def access_token():
#     print request.form
#     print server.create_access_token_response(
#         request.url,
#         request.method,
#         request.form,
#         request.headers,
#     )
    # return make_response(jsonify({}), 200)


@app.route('/access_token', methods=['POST'])
def access_token():
    _, h, b, s = server.create_access_token_response(
        request.url,
        http_method=request.method,
        body=request.data,
        headers={
            u'Authorization': 'OAuth oauth_token=asiuydgjhaghjsgdjhga,oauth_verifier=ahskdhaksdaskdjaasdfew,oauth_signature=thing&other-thing,oauth_consumer_key=asjhgdahjgsduyrughjadkjhk,oauth_nonce=asjhdgjhajhsdgjajhgjhgsjhg,oauth_timestamp={},oauth_signature_method=PLAINTEXT'.format(int(time.time()))
        }
    )
    return Response(b, status=s, headers=h)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
