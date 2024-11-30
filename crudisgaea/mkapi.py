import dataclasses
import http.client
from typing import Type

import flask

import crudisgaea.store

def mkapis(dc: Type, singular: str, plural: str) -> tuple[flask.Blueprint, flask.Blueprint]:
    api_singular_bp = flask.Blueprint(singular, "crudisgaea")
    api_plural_bp = flask.Blueprint(plural, "crudisgaea")

    # Plural has GET for listing (Read) and POST for adding (Create)
    @api_plural_bp.route(f"/{plural}", methods=["GET", "POST"])
    def handle_dc_group():
        crudisgaea.store.ensure_store()
        content_type = "application/json"
        response = {}
        response_code = http.client.OK
        if (flask.request.method == "GET"):
            response = {
                "items": [{"id": id, dc.__name__: dataclasses.asdict(data)} for id, data in flask.g.store.list(dc)]
            }
        elif (flask.request.method == "POST"):
            try:
                data_id, data = flask.g.store.put(dc(**flask.request.get_json(force=True)))
                response = {
                    "id": data_id,
                    dc.__name__: dataclasses.asdict(data)
                }
            except ValueError:
                response = {"error": "serialization failure"}
                response_code = http.client.BAD_REQUEST
        
        return (flask.json.dumps(response), response_code, {"Content-Type": content_type})
    
    # Singular has GET for Read, POST/PUT for Create/Update, DELETE for... delete.
    @api_singular_bp.route(f"/{singular}/<data_id>", methods=["GET", "POST", "PUT", "DELETE"])
    def handle_dc_req(data_id: str):
        crudisgaea.store.ensure_store()
        content_type = "application/json"
        response_code = http.client.OK
        response = {}
        if (flask.request.method == "GET"):
            try:
                response = dataclasses.asdict(flask.g.store.get(dc, data_id))
            except crudisgaea.store.ItemDoesntExist:
                response = {"error": "item not found"}
                response_code = http.client.NOT_FOUND
        elif (flask.request.method in ("POST", "PUT")):
            try:
                data_id, data = flask.g.store.put(dc(**flask.request.get_json(force=True)), data_id)
                response = {
                    "id": data_id,
                    dc.__class__.__name__: dataclasses.asdict(data)
                }
            except ValueError:
                response = {"error": "serialization failure"}
                response_code = http.client.BAD_REQUEST
        elif (flask.request.method == "DELETE"):
            try:
                response = {"success": flask.g.store.delete(dc, data_id)}
            except crudisgaea.store.ItemDoesntExist:
                response = {"success": "false", "error": "item not found"}
                response_code = http.client.NOT_FOUND
        
        return (flask.json.dumps(response), response_code, {"Content-Type": content_type})
    
    return (api_singular_bp, api_plural_bp)