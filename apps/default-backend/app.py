import json
import os
from flask import Flask, request, Response

app = Flask(__name__)

NAME = os.getenv('NAME')

@app.route('/', methods=['GET', 'POST'])
def error():
    code = request.headers.get('X-Code')
    orig_url = request.headers.get('X-Original-Uri')
    error_message = f'Error : {code}'

    if code == '401' or code == '403':
        error_message = 'Not Authorized'

    return Response(json.dumps({
        'status': 'error',
        'name': NAME,
        'error': error_message,
    }), status=code)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)