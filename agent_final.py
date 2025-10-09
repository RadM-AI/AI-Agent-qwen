from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
from langchain_core.runnables.base import Runnable
from typing import Optional, Any
from langchain_core.runnables import RunnableConfig
from langchain.memory import ConversationBufferMemory
import json
import logging
from tool import *
from prompts import *

class ToolCall(BaseModel):
    tool: Literal["get_weather", "search_information", "calculate"]
    input: str

class TrimResponseRunnable(Runnable):
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        text = input
        if hasattr(text, "content"):
            text.content = text.content
        start_pos = text.content.find('<|im_start|>assistant')
        if start_pos != -1:
            text.content = text.content[start_pos+len('<|im_start|>assistant'):]
        return text

trim_response = TrimResponseRunnable()

def parse_ai_response(response_text: str) -> Optional[ToolCall]:
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
        tool_call = ToolCall(**data)

        # Дополнительные проверки бизнес-логики
        if not is_valid_input(tool_call.tool, tool_call.input):
            logging.warning(f"Invalid input for tool {tool_call.tool}: {tool_call.input}")
            return None

        return tool_call

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON from AI: {e}")
        return None
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


def get_result(responce):

  ask_chain = ask_result_quest | chat_model | trim_response


  result = ask_chain.invoke({
      "user_question": resp['input'],
      "previous_result": responce
  })
  return result.content

def is_valid_input(tool_name: str, input_data: str) -> bool:
    """Проверяет корректность входных данных для конкретного инструмента"""

    validators = {
        "get_weather": lambda x: len(x.strip()) > 0 and x.isprintable(),
        "search_information": lambda x: len(x.strip()) >= 2,
        "calculate": lambda x: is_valid_expression(x)
    }

    validator = validators.get(tool_name)
    return validator(input_data) if validator else False

def is_valid_expression(expr: str) -> bool:
    """Проверяет безопасность математического выражения"""

    dangerous_keywords = ['import', 'exec', 'eval', '__', 'open', 'file']
    return all(keyword not in expr for keyword in dangerous_keywords)


def format_tools_description(tools_list):
    descriptions = []
    for tool in tools_list:
        desc = f"""{tool.name}:
   - Description: {tool.description}
   - Input data: {', '.join([f'{param_name}: {param_type}' for param_name, param_type in tool.args.items()])}"""
        descriptions.append(desc)
    return "\n\n".join(descriptions)


def process_ai_response(ai_response: str):
    """
    Основной процесс обработки ответа ИИ
    """

    if '[TOOL]' in ai_response:
      start = ai_response.find('[TOOL]')
      ask = ai_response[start+7:].strip()
      tool_call = parse_ai_response(ask)

      if not tool_call:

          return {"error": "Invalid AI response"}


      try:
          result = execute_tool(tool_call.tool, tool_call.input)
          result = get_result(result)
          return result
      except Exception as e:
          logging.error(f"Tool execution failed: {e}")
          return {"error": f"Tool execution failed: {str(e)}"}

    else:
      return ai_response

def execute_tool(tool_name: str, input_data: str):
    """Выполняет конкретный инструмент"""

    tools = {
        "get_weather": get_weather,
        "search_information": search_information,
        "calculate": calculate
    }

    if tool_name not in tools:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tools[tool_name].invoke(input_data)


class ProcessAIResponse(Runnable):
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        text = input
        if hasattr(text, "content"):
            text.content = text.content
        text.content = process_ai_response(text.content)
        return text
process = ProcessAIResponse()


pipe = pipeline(
    "text-generation",
    'Qwen/Qwen2.5-3B-Instruct',
    temperature = 0.001,
    max_new_tokens=1000,
    device=0,
)

hf_pipeline = HuggingFacePipeline(pipeline=pipe)
chat_model = ChatHuggingFace(llm=hf_pipeline,)


tools = [calculate, get_weather, search_information]

tools_description = format_tools_description(tools)


prompt_template = PromptTemplate(
    template=(main_prompt),
    input_variables=['input'],
    partial_variables={'tools_description': tools_description},
)


ask_result_quest = PromptTemplate(
    input_variables=["user_question", "previous_result"],
    template=(
        "Был вопрос пользователя:\n{user_question}\n"
        "Из инструмента ты выяснил, что:\n{previous_result}\n"
    )
)


memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="history",
    input_key="input"
)
chain = prompt_template | chat_model | trim_response | process
resp = {}
def chat_with_memory():
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == 'выход':
            break
        resp['input'] = user_input
        # Получаем историю из памяти
        history = memory.load_memory_variables({})["history"]
        history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in history])

        # Генерируем ответ
        response = chain.invoke({
            "input": user_input,
            "history": history_text
        })

        print(f"Ассистент: {response.content}")

        # Сохраняем в память
        memory.save_context({"input": user_input}, {"output": response.content})


chat_with_memory()