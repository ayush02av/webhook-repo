from flask import Blueprint, render_template

ui = Blueprint('ui', __name__, url_prefix='')

@ui.route('/', methods=["GET"])
def user_interface():
    return render_template('index.html')