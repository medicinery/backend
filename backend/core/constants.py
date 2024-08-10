import os
from dotenv import load_dotenv

load_dotenv()

IBM_WATSON_API_KEY = os.getenv("IBM_WATSON_API_KEY")
IBM_WATSON_URL = os.getenv("IBM_WATSON_URL")
IBM_WATSON_VERSION = os.getenv("IBM_WATSON_VERSION")

IBM_WATSON_ASSISTANT_ID = os.getenv("IBM_WATSON_ASSISTANT_ID")
IBM_WATSON_SESSION_ID = os.getenv("IBM_WATSON_SESSION_ID")
