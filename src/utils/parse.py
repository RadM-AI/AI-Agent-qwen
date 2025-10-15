import json
import logging
from typing import Optional
from pydantic import ValidationError

from .validators import is_valid_input
from ..models.schemas import ToolCall


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_ai_response(response_text: str) -> Optional[ToolCall]:
    """
    Безопасно парсит ответ ИИ и валидирует его
    """
    try:
        # Пытаемся распарсить JSON
        cleaned_response = response_text.strip()

        # Убираем возможные markdown блоки кода
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]  # убираем ```json
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # убираем ```
        cleaned_response = cleaned_response.strip()

        data = json.loads(cleaned_response)

        # Валидируем через Pydantic
        tool_call = ToolCall(**data)

        # Дополнительные проверки бизнес-логики
        if not is_valid_input(tool_call.tool, tool_call.input):
            logging.warning(f"Invalid input for tool {tool_call.tool}: {tool_call.input}")
            return None

        return tool_call

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON from AI: {e}")
        return None
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None