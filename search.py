from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

class QwenEmbeddings(Embeddings):
    def __init__(self, model_name="Qwen/Qwen3-Embedding-0.6B"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text):
        embeddings = self.model.encode([text], prompt_name="query")
        return embeddings[0].tolist()

    def embed_documents(self, texts):
        embeddings = self.model.encode(texts)
        return [e.tolist() for e in embeddings]


embeddings = QwenEmbeddings()

def faiss_search(query, max_results=3):
    db = FAISS.load_local('/content/faiss_index', embeddings, allow_dangerous_deserialization=True)
    result = db.similarity_search_with_score(query, k=max_results)
    res = ''
    for i,r in enumerate(result, start= 1):
        title = r[0].page_content
        r = r[0].metadata
        res+=str(i)+':\n'
        res+=f"Заголовок: {r.get('title')}\n"
        res+=f"Новость: {r.get('text')}\n"
        res+=f"Ссылка: {r.get('url')}\n"
        res+='\n'
    res = '''

Задача: На основе РЕЗУЛЬТАТА ПОИСКА сформируй для пользователя структурированный ответ по новостям.

Основные требования:

1. Анализ: Проанализируй каждую новость из результатов поиска. Выдели главные темы и ключевую информацию по каждой новости.

2. Структура ответа: Для каждой новости предоставь:
   - Основная тема/заголовок
   - Краткое описание (2-3 предложения) с самой важной информацией
   - Ссылка на источник

3. Приоритеты: В первую очередь отрази:
   - Главные события и факты
   - Ключевые детали, которые имеют значение
   - Важные даты, места, участники событий

4. Требования к формату:
   - Ответ должен быть четко структурирован по новостям
   - Для каждой новости обязательно краткое описание (2-3 предложения) + ссылка
   - Сохраняй только проверенные факты из результатов поиска
   - Избегай дублирования информации

5. Запрещено: придумывать информацию, добавлять детали не из результатов поиска, изменять ссылки.

РЕЗУЛЬТАТ ПОИСКА для анализа:\n
'''+res
    
    return res
