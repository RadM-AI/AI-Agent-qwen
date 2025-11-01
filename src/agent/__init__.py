"""
Модуль агента - основная логика обработки запросов и управления диалогом
"""

from .core import AIAgent
from .registr_agent import AgentRegistry
from .memory import ManageMemory
from .response_processor import ResponseProcessor

__all__ = [
    "AgentRegistry",
    "AIAgent",
    "ManageMemory", 
    "ResponseProcessor",
]