from flask import Flask, Response, request
from hashlib import sha1
import base64
import hmac
import os
import requests


app = Flask(__name__)
app.debug = os.getenv('DEBUG', '') == 'True'


def fetch_image(out_path):
    chunk_size = 1024

    r = requests.get(out_path, stream=True, params=request.args)
    headers = dict(r.headers)

    def generate():
        for chunk in r.iter_content(chunk_size):
            yield chunk

    return Response(generate(), headers=headers)


@app.route('/healthcheck')
def serve_image(config, uri):
    return 'WORKING'


@app.route('/t/<path:config>/u/<path:uri>')
def serve_image(config, uri):
    key = os.environ['THUMBOR_SECURITY_KEY']
    image_path = os.environ['BACKEND_ASSET_PATH'] + '/' + uri
    config_with_path = config + '/' + image_path
    mac = base64.urlsafe_b64encode(hmac.new(key.encode(), config_with_path.encode(), sha1).digest())
    out_path = 'https://' + os.environ['THUMBOR_PATH'] + '/' + mac.decode('utf-8') + '/' + config_with_path
    if app.debug:
        print('serving ' + out_path)

    return fetch_image(out_path)


if __name__ == '__main__':
    app.run()

