import os

import flask

import crudisgaea.mkapi
import crudisgaea.model
import crudisgaea.store
import crudisgaea.auth

__all__ = ["app"]

app = flask.Flask("crudisgaea")
if os.environ.get("API_AUTH_KEY") is not None:
    app.wsgi_app = crudisgaea.auth.auth(app.wsgi_app)
else:
    app.logger.warning("WARNING: No API_AUTH_KEY specified, all requests allowed")

char_apis = crudisgaea.mkapi.mkapis(crudisgaea.model.DisgaeaCharacter, "character", "characters")

for char_api in char_apis:
    app.register_blueprint(char_api, url_prefix='/v1')

app