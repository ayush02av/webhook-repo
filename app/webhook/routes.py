from flask import Blueprint
from ..extensions import mongo
from ..utility import get_action_object

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    '''Webhook to receive github-action events and store in database'''
    
    # get the serialized action-object
    action_object = get_action_object()
    # store the action-object in Mongo Database
    mongo.db.action.insert_one(action_object)

    return {
        "action_recorded": action_object['action']
    }, 200