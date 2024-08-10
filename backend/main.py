from flask import Flask
from flask_cors import CORS


from backend.core.firebase import init_firebase
from backend.handlers.before_request import before_request
from backend.routes.chat import bp_chat


# -----------------------------------------------------------------------------

init_firebase()

# -----------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# -----------------------------------------------------------------------------
# Health check endpoint
# -----------------------------------------------------------------------------


@app.route("/health")
def health():
    return "OK", 200


# -----------------------------------------------------------------------------
# Register before request handler for authentication
# -----------------------------------------------------------------------------

app.before_request(before_request)


# -----------------------------------------------------------------------------
# Register blueprints
# -----------------------------------------------------------------------------

app.register_blueprint(bp_chat, url_prefix="/chat")

# -----------------------------------------------------------------------------
# Serve
# -----------------------------------------------------------------------------


def main():
    app.run(debug=True)


# -----------------------------------------------------------------------------
