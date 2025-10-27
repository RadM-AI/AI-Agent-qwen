from .base import BaseTool
from search import faiss_search  # Импортируем вашу существующую функцию

class SearchTool(BaseTool):
    """Инструмент для поиска информации"""

    @property
    def name(self) -> str:
        return "search_information"
    
    @property
    def description(self) -> str:
        return """Search for information on a given query.
        Args:
            input_data: A search query in Russian

        Returns:
            Information found
        """
    
    def execute(self, input) -> str:
        print('Уже ищу!')
        try:
            inp, emb_model = input
            resp = faiss_search(input, emb_model)
            return resp
        except Exception as e:
            return f"Ошибка поиска: {str(e)}"
