"""
AI Agent Project
Многофункциональный агент с инструментами для поиска, вычислений и погоды
"""

from .agent.core import AIAgent
from .tools.registry import ToolRegistry
from .models.schemas import ToolCall, ChatMessage

__version__ = "1.0.0"
__author__ = "RadAI"
__all__ = [
    "AIAgent",
    "ToolRegistry", 
    "ToolCall",
    "ChatMessage",
]