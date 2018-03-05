from flask import request
from flask_jwt_extended import jwt_required

import walkoff.case.database as case_database
from walkoff.server.returncodes import *
from walkoff.security import permissions_accepted_for_resources, ResourcePermissions
from walkoff.server.decorators import validate_resource_exists_factory

validate_event_exists = validate_resource_exists_factory(
    'event',
    lambda event_id: case_database.case_db.session.query(case_database.Event).filter(
        case_database.Event.id == event_id).first())


def update_event_note():
    data = request.get_json()
    event_id = data['id']

    @jwt_required
    @permissions_accepted_for_resources(ResourcePermissions('cases', ['update']))
    @validate_event_exists('update', event_id)
    def __func():
        case_database.case_db.edit_event_note(event_id, data['note'])
        return case_database.case_db.event_as_json(event_id), SUCCESS

    return __func()


def read_event(event_id):
    @jwt_required
    @permissions_accepted_for_resources(ResourcePermissions('cases', ['read']))
    @validate_event_exists('read', event_id)
    def __func():
        return case_database.case_db.event_as_json(event_id), SUCCESS

    return __func()
