"""
Модуль агента - основная логика обработки запросов и управления диалогом
"""

from .core import AIAgent
from .memory import ConversationManager
from .response_processor import ResponseProcessor

__all__ = [
    "AIAgent",
    "ConversationManager", 
    "ResponseProcessor",
]