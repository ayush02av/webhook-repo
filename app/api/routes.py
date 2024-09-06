from flask import Blueprint, json, request
from ..extensions import mongo

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('', methods=["GET"])
def get_actions():
    actions = []
    for action in mongo.db.action.find().sort({'timestamp': -1}):
        action['timestamp'] = action['timestamp'].strftime(f'%d %B %Y - %I:%M %p UTC')
        actions.append(action)
    
    return {
        "actions": json.loads(json.dumps(actions, default=str))
    }, 200