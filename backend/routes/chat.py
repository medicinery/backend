import datetime
from flask import Blueprint, request, jsonify

from backend.core.pool import run_in_thread
from backend.core.llm import ask_llm
from backend.core.utils import generate_id
from backend.core.firebase import db
from backend.models.user import User
from backend.models.chat import Chat, ChatMessage, ChatMessageRole


bp_chat = Blueprint("chat", __name__)


@bp_chat.route("/create")
def create():
    user_id = getattr(request, "userID", None)
    if user_id is None:
        return jsonify({"message": "Unauthorized"}), 401

    user_data = db.collection("Users").document(user_id).get().to_dict()
    user_name = User.model_validate(user_data).name

    chat = Chat(
        id=generate_id(),
        title="New Chat",
        createdBy=user_name,
        createdAt=datetime.datetime.now(),
        messages=[],
    )
    db.collection("Chats").document(chat.id).set(chat.model_dump())

    return jsonify({"message": "Chat created", "chat_id": chat.id}), 200


@bp_chat.route("/delete/<string:chat_id>")
def delete(chat_id: str):
    try:
        db.collection("Chats").document(chat_id).delete()
    except Exception as e:
        return jsonify({"message": "Chat not found"}), 404

    return jsonify({"message": "Chat deleted", "chat_id": chat_id}), 200


def process_chat(chat_id: str) -> None:
    # Check for chat's existence
    doc_ref = db.collection("Chats").document(chat_id)
    doc = doc_ref.get()
    if not doc.exists:
        return

    # Fetch the chat
    doc_data = Chat.model_validate(doc.to_dict())
    last_message = doc_data.messages[-1]
    if not last_message.isUnderProcess or last_message.role == ChatMessageRole.user:
        return

    # Process the chat
    query = doc_data.messages[-2].message
    response = ask_llm(query)
    if response is None:
        last_message.message = "Sorry, I am not able to process your request."
    else:
        last_message.message = response
    last_message.isUnderProcess = False

    # Update the chat
    doc_ref.set(doc_data.model_dump())


@bp_chat.route("/push_message/<string:chat_id>")
def push_message(chat_id):
    run_in_thread(process_chat)(chat_id)

    # Check for chat's existence
    doc_ref = db.collection("Chats").document(chat_id)
    doc = doc_ref.get()
    if not doc.exists:
        return jsonify({"message": "Chat not found"}), 404

    # Fetch the chat
    doc_data = Chat.model_validate(doc.to_dict())
    last_message = doc_data.messages[-1]
    if last_message.role == ChatMessageRole.user:
        return jsonify({"message": "Cannot push message"}), 403

    # Push user's message
    body = request.get_json()
    user_message = None
    try:
        user_message = ChatMessage.model_validate(body, strict=True)
    except Exception as e:
        return jsonify({"message": "Invalid message content"}), 400
    doc_data.messages.append(user_message)

    # Push system's message
    system_message = ChatMessage(
        id=generate_id(),
        createdAt=user_message.createdAt,
        role=ChatMessageRole.system,
        createdBy="System",
        isUnderProcess=True,
        message="What is your name?",
        suggestions={},
    )
    doc_data.messages.append(system_message)

    # Update the chat
    doc_ref.set(doc_data.model_dump())

    run_in_thread(process_chat)(chat_id)

    return jsonify({"message": "Success"}), 200
