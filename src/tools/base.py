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
    
    @property
    @abstractmethod
    def args(self) -> dict:
        pass
    
    @abstractmethod
    def invoke(self, input_data: str) -> Any:
        pass
    
    def to_langchain_tool(self):
        """Конвертирует инструмент в LangChain tool"""
        @tool
        def langchain_tool(input: str) -> str:
            return self.invoke(input)
        
        # Устанавливаем метаданные
        langchain_tool.name = self.name
        langchain_tool.description = self.description
        return langchain_tool