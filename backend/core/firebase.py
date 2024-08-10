from firebase_admin import credentials, initialize_app
from firebase_admin.firestore import client


def init_firebase():
    cred = credentials.Certificate("./credentials.json")
    initialize_app(cred)


db = client()
