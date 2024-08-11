from firebase_admin import credentials, auth
from flask import request, jsonify


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
