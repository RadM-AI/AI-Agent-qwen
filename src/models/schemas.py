from pydantic import BaseModel
from typing import Literal, Optional


class ToolCall(BaseModel):
    tool: Literal["get_weather", "search_information", "calculate"]
    input: str

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatResponse(BaseModel):
    content: str
    tool_calls: Optional[list[ToolCall]] = None

class RedirectAgent(BaseModel):
    agent: str
    request: str
