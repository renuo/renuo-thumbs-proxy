# Renuo Thumbs Proxy

Renuo thumbs proxy is an app to sign images so they are processed by thumbor. You can restrict the source of the images by setting
the BACKEND_IMAGES_PATH (e.g. ao3ief5j.cloudfront.com), so only images from this domain / path are processed by thumbor.

## Deployment

The app is ready to run on heroku. Create a new heroku app, set the env variables, and push the code to Heroku.

### Performance / Requests per Second

With the default heroku host (1 dyno for the proxy, 1 dyno for thumbor), about 20 rps are possible.

## Installation and Usage

* Install pyenv
* cp local_server.example.sh local_server.sh
* Adjust config for local_server.sh

```sh
pyenv install
pip install -r requirements.txt
THUMBOR_SECURITY_KEY=UJwHAZLsRejTyLI88lAriHL7xAXa6q0umiwwpPcP \
 BACKEND_ASSET_PATH=ao3ief5j.cloudfront.com \
 THUMBOR_PATH=thumbor.example.com \
 DEBUG=True \
 python server.py
```

* Create a backend and upload images (e.g. S3)
* Make the images accessible (e.g. Cloudfront)
** From this step, you will get the BACKEND_ASSET_PATH, e.g. ao3ief5j.cloudfront.com
* Generate a THUMBOR_SECURITY_KEY, configure thumbor
* Transform images calling the right url (/thumb/<path:config>/u/<path:uri>)
** Example: /thumb/200x300/smart/u/images/logo.png


## Config

The configuration is done by setting environment variables.

Example:

```
THUMBOR_SECURITY_KEY=UJwHAZLsRejTyLI88lAriHL7xAXa6q0umiwwpPcP
BACKEND_ASSET_PATH=ao3ief5j.cloudfront.com
```

### THUMBOR_SECURITY_KEY

The THUMBOR_SECURITY_KEY is a shared key (proxy and thumbor app) to validate
that the image can be processed by thumbor.

In thumbor this key is called SECURITY_KEY. See also: https://github.com/thumbor/thumbor/wiki/Security

Generate it randomly, and keep it secret (only shared with the thumbor app).

Example: UJwHAZLsRejTyLI88lAriHL7xAXa6q0umiwwpPcP

### BACKEND_IMAGES_PATH

The BACKEND_IMAGES_PATH is the host and the path from which the assets are
downloaded. E.g. if you want to resize images from the site https://www.renuo.ch,
e.g. https://www.renuo.ch/images/logo.png then you can define

1. the BACKEND_IMAGES_PATH to "www.renuo.ch", and then make a request to images/logo.png
2. the BACKEND_IMAGES_PATH to "www.renuo.ch/images", and then make a request to logo.png

Don't leave it blank. Don't use http:// or https:// in the path.

### THUMBOR_PATH

This is the path to your thumbor server.

Example: thumbor.example.com

### DEBUG

Optional.

Example: True

## Design Decisions

* Use HTTPS everywhere
* Have only one host to serve images which should be resized
* Have one thumbor instance which resizes images

## Renuo Thumbor

See https://github.com/renuo/renuo-thumbor
