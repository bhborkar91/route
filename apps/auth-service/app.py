import json
import os
from flask import Flask, request, Response

app = Flask(__name__)

NAME = os.getenv('NAME')
AUTH_USER = os.getenv('AUTH_USER', None)

@app.route('/authorize', methods=['GET'])
def authorize():
    user = request.headers.get('user')
    if AUTH_USER is None or user == AUTH_USER:
        return Response(json.dumps({'status': 'ok', 'name': NAME}), status=200)
    else:
        return Response(json.dumps({'status': 'notauthorized', 'name': NAME}), status=401)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
