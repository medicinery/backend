from flask import Blueprint
from flask_cors import CORS

from backend.routes.chat import bp_chat
from backend.handlers.before_request import before_request


# -----------------------------------------------------------------------------

bp_app = Blueprint("root", __name__)
CORS(bp_app, resources={r"/*": {"origins": "*"}})


# -----------------------------------------------------------------------------
# Register before request handler for authentication
# -----------------------------------------------------------------------------

bp_app.before_request(before_request)


# -----------------------------------------------------------------------------
# Register blueprints
# -----------------------------------------------------------------------------

bp_app.register_blueprint(bp_chat, url_prefix="/chat")

# -----------------------------------------------------------------------------
