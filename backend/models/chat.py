from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum


class ChatMessageRole(str, Enum):
    user = "User"
    system = "System"


class ChatMessage(BaseModel):
    id: str = Field(..., alias="id")
    createdBy: str = Field(..., alias="createdBy")
    createdAt: int = Field(
        ..., alias="createdAt"
    )  # Assume Unix timestamp, handle conversion if necessary
    role: ChatMessageRole = Field(..., alias="role")
    isUnderProcess: bool = Field(..., alias="isUnderProcess")
    message: str = Field(..., alias="message")
    suggestions: Dict[str, Any] = Field(..., alias="suggestions")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class Chat(BaseModel):
    id: str = Field(..., alias="id")
    createdBy: str = Field(..., alias="createdBy")
    createdAt: int = Field(
        ..., alias="createdAt"
    )  # Same assumption as above for the timestamp
    title: str = Field(..., alias="title")
    messages: List[ChatMessage] = Field(..., alias="messages")

    class Config:
        allow_population_by_field_name = True
