from flask import Blueprint
from flask_cors import CORS

from backend.routes.chat import bp_chat


# -----------------------------------------------------------------------------

bp_app = Blueprint("root", __name__)
CORS(bp_app, resources={r"/*": {"origins": "*"}})


# -----------------------------------------------------------------------------
# Register before request handler for authentication
# -----------------------------------------------------------------------------


@bp_app.before_request
def before_request():
    # setattr(request, "userID", "aqE2MxBnijRk7cZbP3lQj63RIyF2")

    return None

    if request.endpoint == "health":
        return None

    id_token = request.headers.get("Authorization-Token")
    if not id_token:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        decoded_token = auth.verify_id_token(id_token)
        setattr(request, "userID", decoded_token)
    except Exception as e:
        print("Token verification failed:", e)
        return jsonify({"error": "Invalid ID token"}), 401

    return None


# -----------------------------------------------------------------------------
# Register blueprints
# -----------------------------------------------------------------------------

bp_app.register_blueprint(bp_chat, url_prefix="/chat")

# -----------------------------------------------------------------------------
