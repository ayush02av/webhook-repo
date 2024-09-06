from flask import Flask
from flask_cors import CORS

from app.webhook.routes import webhook
from app.api.routes import api
from app.ui.routes import ui

# Creating our flask app
def create_app():

    app = Flask(__name__)
    CORS(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(api)
    app.register_blueprint(ui)
    
    return app
