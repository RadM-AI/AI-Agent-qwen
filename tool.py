from langchain.tools import tool
import requests
import json
from weather import get
from search import duckduckgo_search
@tool
def get_weather(input: str) -> str:
    """Get the current weather for the specified city.

    Args:
        input: The name of the city in Engilsh (for example: 'Moscow', 'Samara')

    Returns:
        A line with information about temperature and weather conditions
    """
    try:
        # Демо-версия без реального API
        weather_data = get(input)
        return weather_data
    except Exception as e:
        return f"Ошибка: {str(e)}"

@tool
def calculate(input: str) -> str:
    """Calculate a mathematical expression.

    Args:
        input: A mathematical expression (for example: '2 + 2 * 3', ' sin(45)')

    Returns:
        Calculation result
    """
    try:
        print('Начал считать...')
        allowed_chars = set('0123456789+-*/.() ')
        if all(c in allowed_chars for c in input):
            result = eval(input)
            return f"ОТВЕТ КРАТКИЙ: Результат: {input} = {result}"
        else:
            return "Ошибка: выражение содержит недопустимые символы"
    except Exception as e:
        return f"Ошибка вычисления: {str(e)}"

@tool
def search_information(input: str) -> str:
    """Search for information on a given query.

    Args:
        input: A search query in Russian

    Returns:
        Information found
    """
    resp = duckduckgo_search(input)
    return resp

