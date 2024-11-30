
import http.client
import os
from typing import Callable

import flask
import werkzeug.wrappers

def auth(wsgi_app: flask.Flask) -> Callable:
    def auth_middleware(environ, start_response):
        req = werkzeug.wrappers.Request(environ)
        if req.headers.get("X-Api-Key", None) == os.environ["API_AUTH_KEY"]:
            return wsgi_app(environ, start_response)
        else:
            start_response(f"{http.client.FORBIDDEN} Forbidden", [('Content-Type', 'application/json')])
            return [flask.json.dumps({"error": "authentication failed"}).encode("utf-8")]
    
    return auth_middleware