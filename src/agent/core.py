from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import PromptTemplate

from ..config.settings import settings
from ..config.prompts import main_prompt, ask_result_prompt
from .memory import ManageMemory
from .response_processor import ResponseProcessor, TrimResponseRunnable
from ..tools.registry import ToolRegistry
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


class AIAgent:
    def __init__(self):
        self.embed_model = QwenEmbeddings()
        self.chat_model = self._setup_model()
        self.tool_registry = ToolRegistry()
        self.tool_desctiption = ToolRegistry().get_tools_description()
        self.memory = ManageMemory().memory
        self.response_processor = ResponseProcessor(self.tool_registry, self.embed_model)
        self.chain = self._build_chain()
        self.trim_resp = TrimResponseRunnable()
    
    def _setup_model(self):
        pipe = pipeline(
            "text-generation",
            settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            device=settings.DEVICE,
        )
        return ChatHuggingFace(llm=HuggingFacePipeline(pipeline=pipe))
    
    def _build_chain(self):
        prompt_template = PromptTemplate(
            template=main_prompt,
            input_variables=['input'],
            partial_variables={
                'tools_description': self.tool_registry.get_tools_description()
            },
        )
        return prompt_template | self.chat_model | self.response_processor
    
    def _result_ask_ai(self, user_question, previous_result):
        ask_result_quest = PromptTemplate(
            input_variables=["user_question", "previous_result"],
            template=(
                "Был вопрос пользователя:\n{user_question}\n"
                "Из инструмента ты выяснил, что:\n{previous_result}\n"
            )
        )
        chain = ask_result_quest | self.chat_model | self.trim_resp


        return chain.invoke({
            "user_question": user_question,
            "previous_result": previous_result
        })

    def chat(self, user_input: str) -> str:

        history = self.memory.load_memory_variables({})["history"]
        history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in history])
        response = self.chain.invoke({
            "input": user_input,
            "history": history_text
        })

        if hasattr(response, "ai_message"):
            self.memory.save_context({"input": user_input}, {"output": response['ai_message']})
            return response
        
        else:
            response = self._result_ask_ai(user_question=user_input, previous_result=response)   
            self.memory.save_context({"input": user_input}, {"output": response})
            return response
