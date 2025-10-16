from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.base import Runnable
from typing import Any, Optional

from ..utils.parse import parse_ai_response


class TrimResponseRunnable(Runnable):
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        text = input
        if hasattr(text, "content"):
            text.content = text.content
        start_pos = text.content.find('<|im_start|>assistant')
        if start_pos != -1:
            text.content = text.content[start_pos+len('<|im_start|>assistant'):]
        
        return text.content

class ResponseProcessor(Runnable):
    def __init__(self, tool_registry):
        self.tool_registry = tool_registry
    
    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        if hasattr(input, "content"):
            ai_message = input.content
        start_pos = ai_message.find('<|im_start|>assistant')
        if start_pos != -1:
            ai_message = ai_message[start_pos+len('<|im_start|>assistant'):]
            ai_message = self._process_ai_message(ai_message)
        return ai_message
    
    def _process_ai_message(self, ai_message: str):
        """
        Основной процесс обработки ответа ИИ
        """

        if '[TOOL]' in ai_message:
            start = ai_message.find('[TOOL]')
            ask = ai_message[start+7:].strip()
            tool_call = parse_ai_response(ask)

            if not tool_call:

                return {"error": "Invalid AI response"}

            try:
                result = self.tool_registry.execute_tool(tool_call.tool, tool_call.input)
                return result
            except Exception as e:
                return {"error": f"Tool execution failed: {str(e)}"}

        else:
            return {"ai_message": ai_message}