from ibm_watson import AssistantV2
from ibm_watson.assistant_v2 import MessageInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from backend.core.constants import (
    IBM_WATSON_API_KEY,
    IBM_WATSON_URL,
    IBM_WATSON_VERSION,
    IBM_WATSON_ASSISTANT_ID,
    IBM_WATSON_SESSION_ID,
)


authenticator = IAMAuthenticator(IBM_WATSON_API_KEY)
assistant = AssistantV2(version=IBM_WATSON_VERSION, authenticator=authenticator)
assistant.set_service_url(IBM_WATSON_URL)


def ask_llm(query: str) -> str | None:
    # Grab the response from the assistant
    response = assistant.message(
        assistant_id=IBM_WATSON_ASSISTANT_ID,
        session_id=IBM_WATSON_SESSION_ID,
        input=MessageInput(text=query),
    ).get_result()

    # If the assistant was unable to respond, no point in continuing
    if response is None:
        return None

    # Extract the response from the assistant
    answer = None
    try:
        answer = response["output"]["generic"][0]["text"]  # type: ignore
    except Exception as e:
        pass

    # Return the response
    return answer
