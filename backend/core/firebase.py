from firebase_admin import credentials, initialize_app


def init_firebase():
    cred = credentials.Certificate("./credentials.json")
    initialize_app(cred)
