import requests
import json
from .base import BaseTool
from weather import get  # Импортируем вашу существующую функцию

class WeatherTool(BaseTool):
    """Инструмент для получения информации о погоде"""
    
    @property
    def name(self) -> str:
        return "get_weather"
    
    @property
    def description(self) -> str:
        return "Get the current weather for the specified city."
    
    @property
    def args(self) -> dict:
        return {"city": "string"}
    
    def invoke(self, input_data: str) -> str:
        """Get the current weather for the specified city.

        Args:
            input_data: The name of the city in English (for example: 'Moscow', 'Samara')

        Returns:
            A line with information about temperature and weather conditions
        """
        try:
            weather_data = get(input_data)
            return weather_data
        except Exception as e:
            return f"Ошибка получения погоды: {str(e)}"