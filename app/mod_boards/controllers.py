from flask import Blueprint

blueprint = Blueprint("boards", __name__)

@blueprint.route("/")
def hello():
    return "Hello, world!"
