import dataclasses
from typing import Any, Optional, Type, Union

import flask

from crudisgaea.model import DisgaeaCharacter, Storable

class SerializationError(ValueError):
    pass


class ItemDoesntExist(ValueError):
    pass


class BackendStore:
    def __init__(self):
        self._typestore = {}

    def put(self, data: Storable, data_id: Optional[str] = None) -> tuple[str, Storable]:
        data_class = data.__class__
        if data_class not in self._typestore:
            self._typestore[data_class] = {}

        if data_id is None:
            data_id = self._identify(data)

        self._typestore[data_class][data_id] = data

        return (data_id, data)
    
    def get(self, data_class: Type, data_id: str) -> Storable:
        try:
            return self._typestore[data_class][data_id]
        except KeyError:
            # either we don't have any of this object type
            # or we don't have this identifier
            # but either way: this object by this id does not exist
            raise ItemDoesntExist
    
    def list(self, data_class: Type) -> list[tuple[str, Storable]]:
        try:
            return [(k, v) for k, v in self._typestore[data_class].items()]
        except KeyError:
            # we don't have this object type stored yet
            # so it's an empty list
            return []
    
    def delete(self, data_class: Type, data_id: str) -> bool:
        try:
            if not self._typestore[data_class].pop(data_id, False):
                raise ItemDoesntExist
        except KeyError:
            raise ItemDoesntExist

        return True
    
    def _identify(self, data: Storable) -> str:
        if isinstance(data, DisgaeaCharacter):
            # use the character's name
            return data.name
        else:
            # numeric incrementing identifiers
            try:
                return str(len(self._typestore[data.__class__]))
            except KeyError:
                return '0'

global_store = BackendStore()

def ensure_store():
    # XXX: in the real world we would have a permanent external store
    # but here we're emulating one with a module-local and inserting it
    # like we would have with the proper permanent external store
    if not hasattr(flask.g, 'store'):
        flask.g.store = global_store