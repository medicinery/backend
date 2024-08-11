import os
from dotenv import load_dotenv

load_dotenv()

IBM_WATSON_API_KEY = os.getenv("IBM_WATSON_API_KEY") or ""
assert IBM_WATSON_API_KEY is not ""

IBM_WATSON_URL = os.getenv("IBM_WATSON_URL") or ""
assert IBM_WATSON_URL is not ""

IBM_WATSON_VERSION = os.getenv("IBM_WATSON_VERSION") or ""
assert IBM_WATSON_VERSION is not ""

IBM_WATSON_ASSISTANT_ID = os.getenv("IBM_WATSON_ASSISTANT_ID") or ""
assert IBM_WATSON_ASSISTANT_ID is not ""

IBM_WATSON_SESSION_ID = os.getenv("IBM_WATSON_SESSION_ID") or ""
assert IBM_WATSON_SESSION_ID is not ""
