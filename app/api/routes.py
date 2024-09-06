from flask import Blueprint, json
from ..extensions import mongo

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('', methods=["GET"])
def get_actions():
    '''API to fetch and return all actions from database'''

    # TODO: use timestamp field (or additional serial-like field) to paginate the api.
    
    actions = []
    for action in mongo.db.action.find().sort({'timestamp': -1}):
        # minimize the timestamp field format for UI
        action['timestamp_min'] = action['timestamp'].strftime(f'%d %B %Y - %I:%M %p UTC')
        actions.append(action)
    
    return {
        "actions": json.loads(json.dumps(actions, default=str)) # JSONify the response
    }, 200