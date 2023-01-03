"""Petstore controllers."""

import logging
from typing import Dict, List, Optional

from flask import make_response
from flask.wrappers import Response
from connexion_patch import current_app
from pymongo.collection import Collection, Cursor

from exceptions import NotFound

logger = logging.getLogger(__name__)


def findPets(
    limit: Optional[int] = None,
    tags: Optional[List] = None,
) -> List[Cursor]:
    db_collection: Collection = (
        current_app.foca.db.dbs['petstore']
        .collections['pets'].client
    )
    filter_dict = {} if tags is None else {'tag': {'$in': tags}}
    if not limit:
        limit = 0
    records = db_collection.find(
        filter_dict,
        {'_id': False}
    ).sort([('$natural', -1)]).limit(limit)
    return list(records)


def addPet(pet: Dict) -> Dict:
    db_collection: Collection = (
        current_app.foca.db.dbs['petstore']
        .collections['pets'].client
    )
    counter: int = 0
    ctr = db_collection.find({}).sort([('$natural', -1)])
    if not ctr.count() == 0:
        document: Dict[str, int] = dict(ctr[0])
        counter = document['id'] + 1
    record = {
        "id": counter,
        "name": pet['name'],
        "tag": pet['tag']
    }
    db_collection.insert_one(record)
    del record['_id']
    return record


def findPetById(id: int) -> Optional[Dict]:
    db_collection: Collection = (
        current_app.foca.db.dbs['petstore']
        .collections['pets'].client
    )
    record = db_collection.find_one(
        {"id": id},
        {'_id': False},
    )
    if record is None:
        raise NotFound
    return record


def deletePet(id: int) -> Response:
    db_collection: Collection = (
        current_app.foca.db.dbs['petstore']
        .collections['pets'].client
    )
    record = db_collection.find_one(
        {"id": id},
        {'_id': False},
    )
    if record is None:
        raise NotFound
    db_collection.delete_one(
        {"id": id},
    )
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    return response
