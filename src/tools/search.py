from .base import BaseTool
from search import faiss_search  # Импортируем вашу существующую функцию

class SearchTool(BaseTool):
    """Инструмент для поиска информации"""
    
    @property
    def name(self) -> str:
        return "search_information"
    
    @property
    def description(self) -> str:
        return "Search for information on a given query."
    
    @property
    def args(self) -> dict:
        return {"query": "string"}
    
    def invoke(self, input_data: str) -> str:
        """Search for information on a given query.

        Args:
            input_data: A search query in Russian

        Returns:
            Information found
        """
        print('Уже ищу!')
        try:
            resp = faiss_search(input_data)
            return resp
        except Exception as e:
            return f"Ошибка поиска: {str(e)}"