from abc import ABC, abstractmethod
from typing import Any
from langchain.tools import tool

class BaseTool(ABC):
    """Базовый класс для всех инструментов агента"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, input: str) -> str:
        pass

    def get_tool(self):
        """Создает декорированный @tool метод"""
        # Создаем функцию-обертку
        def tool_function(input) -> str:
            return self.execute(input)
        
        tool_function.__doc__ = self.description
        # Применяем декоратор с правильными параметрами
        decorated_tool = tool(tool_function)
        
        # Устанавливаем атрибуты
        decorated_tool.name = self.name
        decorated_tool.description = self.description
        
        return decorated_tool
