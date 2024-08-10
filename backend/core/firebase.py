from firebase_admin import credentials, initialize_app
from firebase_admin.firestore import client


cred = credentials.Certificate("./credentials.json")
initialize_app(cred)

db = client()


def init_firebase():
    pass
