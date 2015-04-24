from flask import Flask, Response, request
from hashlib import sha1
import base64
import hmac
import requests

app = Flask(__name__)
app.debug = True


def fetch_image(out_path):
    CHUNK_SIZE = 1024

    r = get_source_rsp(out_path)
    headers = dict(r.headers)

    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk

    return Response(generate(), headers=headers)


def get_source_rsp(url):
    return requests.get(url, stream=True, params=request.args)


@app.route('/thumb/<path:config>/u/<path:uri>')
def serve_image(config, uri):
    key = 'UJwHAZLsRejTyLI88lAriHL7xAXa6q0umiwwpPcP'
    # image_path = '300x200/smart/images/logo.png'
    image_path = 'www.renuo.ch/' + uri
    config_with_path = config + image_path
    mac = base64.urlsafe_b64encode(hmac.new(key.encode(), config_with_path.encode(), sha1).digest())
    out_path = 'https://renuo-thumbor-master.herokuapp.com/' + mac.decode('utf-8') + '/' + config_with_path

    return fetch_image(out_path)


if __name__ == '__main__':
    app.run()

