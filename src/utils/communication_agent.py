import json
import logging
from typing import Optional
from pydantic import ValidationError

from .validators import is_valid_input
from ..models.schemas import RedirectAgent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def redirection_agent(response_text: str) -> Optional[RedirectAgent]:
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
        redir_agent = RedirectAgent(**data)
        print(redir_agent)
        # Дополнительные проверки бизнес-логики
        if not is_valid_input(redir_agent.agent, redir_agent.request):
            logging.warning(f"Invalid input for agent {redir_agent.agent}: {redir_agent.request}")
        #     return None

        return redir_agent

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON from AI: {e}")
        return None
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None