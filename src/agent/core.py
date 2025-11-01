from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from ..config.settings import settings
from ..config.prompts import system_prompt
from .memory import ManageMemory
from .response_processor import ResponseProcessor, TrimResponseRunnable
from ..tools.registry import ToolRegistry
from .registr_agent import AgentRegistry

class AIAgent:
    def __init__(self,
                 name="",
                 sys_prompt=system_prompt,
                 agent: AgentRegistry = None,
                 model = None):
        self.system_prompt = sys_prompt
        self.agents = agent
        self.name = name

        self.chat_model = model if model is not None else self._setup_model()
        self.tool_registry = ToolRegistry()
        self.tool_desctiption = ToolRegistry().get_tools_description()
        self.memory = ManageMemory().memory
        self.response_processor = ResponseProcessor(self.tool_registry, self.agents)
        self.chain = self._build_chain()
        self.trim_resp = TrimResponseRunnable()
    
    def _setup_model(self):
        
        from transformers import pipeline
        from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

        pipe = pipeline(
            "text-generation",
            settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            device=settings.DEVICE,
        )
        return ChatHuggingFace(llm=HuggingFacePipeline(pipeline=pipe))
    
    def _build_chain(self):
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human","{input}"),
        ])
        return chat_prompt | self.chat_model | self.response_processor
    
    def _result_ask_ai(self, user_question, previous_result):
        ask_result_quest = PromptTemplate(
            input_variables=["user_question", "previous_result"],
            template=(
                "Был вопрос пользователя:\n{user_question}\n"
                "Агент тебе передал, что:\n{previous_result}\n"
            )
        )
        chain = ask_result_quest | self.chat_model | self.trim_resp


        return chain.invoke({
            "user_question": user_question,
            "previous_result": previous_result
        })

    def chat(self, user_input: str, is_final_agent=True) -> str:

        history = self.memory.load_memory_variables({})["history"]
        history_messages = []
        for msg in history:
            if msg.type == "human":
                history_messages.append(HumanMessage(content=msg.content))
            elif msg.type == "ai":
                history_messages.append(AIMessage(content=msg.content))


        response = self.chain.invoke({
            "input": user_input,
            "history": history_messages
        })
        print(response)
        if is_final_agent and not isinstance(response, dict):
            response = self._result_ask_ai(user_question=user_input, previous_result=response)
        
        # Сохраняем в память
        if isinstance(response, dict) and 'ai_message' in response:
            final_response = response['ai_message']
        else:
            final_response = str(response)
        
        self.memory.save_context({"input": user_input}, {"output": final_response})
        return final_response