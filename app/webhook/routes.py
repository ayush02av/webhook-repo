from flask import Blueprint, json, request
from ..extensions import mongo
from ..utility import get_action_object

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/ping', methods=["GET"])
def ping():
    return {
        "message": "Hello World"
    }, 200

@webhook.route('/receiver', methods=["POST"])
def receiver():
    action_object = get_action_object()
    mongo.db.action.insert_one(action_object)

    return {
        "action_recorded": action_object['action']
    }, 200