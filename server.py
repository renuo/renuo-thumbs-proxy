from flask import Flask, Response, request
from hashlib import sha1
from raven.contrib.flask import Sentry
import base64
import hmac
import os
import requests

def create_app():
    app = Flask(__name__)
    app.debug = os.getenv('DEBUG') == 'True'
    if os.getenv('SENTRY_DSN'):
        sentry = Sentry()
        sentry.init_app(app)
    return app

app = create_app()

def generate(r):
    chunk_size = 1024
    for chunk in r.iter_content(chunk_size):
        yield chunk

def is_image(out_path):
    return extension(out_path) in ['jpg', 'jpeg', 'png', 'gif']

def extension(out_path):
    return out_path.split('.')[-1]

def mime_type_ending(out_path):
    ext = extension(out_path)
    if ext in ['jpg', 'jpeg']:
        return 'jpeg'
    return ext;

def fetch_image(out_path):
    r = requests.get(out_path, stream=True, params=request.args)
    headers = dict(r.headers)
    if is_image(out_path) and headers['content-type'] == "binary/octet-stream":
            headers['content-type'] = "image/" + mime_type_ending(out_path)
    if app.debug:
        print('serving with headers ' + str(headers))
    return Response(generate(r), headers=headers, status=r.status_code)

@app.route('/healthcheck')
def healthcheck():
    return 'WORKING'

@app.route('/o/<path:uri>')
def serve_image_replacing_images_mime_type(uri):
    image_path = 'https://' + os.environ['BACKEND_ASSET_PATH'] + '/o/' + uri
    if app.debug:
            print('serving ' + image_path)
    return fetch_image(image_path)

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
