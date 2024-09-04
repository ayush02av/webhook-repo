from flask import Blueprint, json, request
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    request_json = request.get_json()
    mongo.db.webhooks.insert_one(request_json)
    return {}, 200