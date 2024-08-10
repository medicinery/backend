import os
from dotenv import load_dotenv

load_dotenv()

IBM_WATSON_API_KEY = os.getenv("IBM_WATSON_API_KEY")
assert IBM_WATSON_API_KEY is not ""

IBM_WATSON_URL = os.getenv("IBM_WATSON_URL")
assert IBM_WATSON_URL is not ""

IBM_WATSON_VERSION = os.getenv("IBM_WATSON_VERSION")
assert IBM_WATSON_VERSION is not ""

IBM_WATSON_ASSISTANT_ID = os.getenv("IBM_WATSON_ASSISTANT_ID")
assert IBM_WATSON_ASSISTANT_ID is not ""

IBM_WATSON_SESSION_ID = os.getenv("IBM_WATSON_SESSION_ID")
assert IBM_WATSON_SESSION_ID is not ""
