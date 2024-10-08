from flask import Flask
from flask_cors import CORS

from backend.routes.routes import bp_app

# -----------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# -----------------------------------------------------------------------------
# Register for root blueprint and health check endpoint
# -----------------------------------------------------------------------------

app.register_blueprint(bp_app, url_prefix="/")


@app.route("/health")
def health():
    return "OK", 200


# -----------------------------------------------------------------------------
# Serve
# -----------------------------------------------------------------------------


def main():
    app.run(debug=True)


# -----------------------------------------------------------------------------
