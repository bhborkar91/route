import json
import os
from flask import Flask, request, Response

app = Flask(__name__)

NAME = os.getenv('NAME')

@app.route('/health', methods=['GET'])
def healthcheck():
    return Response(json.dumps({'status': 'ok', 'name': NAME}), status=200)

@app.route('/hello', methods=['GET'])
def hello():
    return Response(json.dumps({'message': f'Hello from {NAME}'}), status=200)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)

