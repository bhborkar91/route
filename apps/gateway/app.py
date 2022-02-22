import json
import os
import threading
import traceback

import requests
from flask import Flask, Response, request

print("Begin execution")

app = Flask(__name__)

NAME = os.getenv('NAME')

base_url = 'https://kubernetes.default'
token = open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r').read()

gates = {}

@app.route('/health', methods=['GET'])
def healthcheck():
    return Response(json.dumps({'status': 'ok', 'name': NAME}), status=200)


# @app.route('/gateway/<url:.*>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def gateway():
#     request.get
#     return Response(json.dumps({'status': 'ok', 'path': NAME}), status=200)

class KubeEventThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True

    def done(self):
        self.is_running = False

    def run(self):
        print("Starting the service")
        try:
            url = '{}/api/v1/services?watch=true"'.format(
                base_url)
            r = requests.get(url, headers={
                'Authorization': f'Bearer {token}'
            }, verify='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt', stream=True)

            print(f'Code = {r.status_code}')
            for line in r.iter_lines():
                if not self.is_running:
                    break
                obj = json.loads(line)
                event_type = obj['type']
                kind = obj['object']['kind']
                if event_type == 'ADDED' and kind == 'Service':
                    meta = obj["object"]["metadata"]
                    label = meta.get('annotations', {}).get('bhborkar91/gateway-config', None)
                    if label is not None:
                        name = obj["object"]["metadata"]["name"]
                        print(f'Found prefix : {label} for service : {name}', flush=True)
        except Exception:
            print('Failure')
            traceback.print_exc()
        print('Done')



if __name__ == '__main__':
    print('Starting the event loop')
    t = KubeEventThread()
    t.start()

    print('Starting the flask server')
    app.run('0.0.0.0', 8080, debug=True)
    t.join()
