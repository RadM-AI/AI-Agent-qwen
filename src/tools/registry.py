from typing import Dict, List
from .base import BaseTool
from .weather import WeatherTool
from .calculator import CalculatorTool
# from .search import SearchTool

class ToolRegistry:
    """Реестр для управления всеми инструментами"""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Регистрирует инструменты по умолчанию"""
        default_tools = [
            WeatherTool().get_tool(),
            CalculatorTool().get_tool(),
            # SearchTool().get_tool()
        ]
        
        for tool in default_tools:
            print(type(tool))
            self.register_tool(tool)
    
    def register_tool(self, tool: BaseTool):
        """Регистрирует новый инструмент"""
        self._tools[tool.name] = tool
    
    def get_tool(self, tool_name: str) -> BaseTool:
        """Возвращает инструмент по имени"""
        if tool_name not in self._tools:
            raise ValueError(f"Инструмент '{tool_name}' не найден")
        return self._tools[tool_name]
    
    def execute_tool(self, tool_name: str, input_data) -> str:
        """Выполняет инструмент"""
        tool = self.get_tool(tool_name)
        return tool.invoke(input_data)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Возвращает все зарегистрированные инструменты"""
        return list(self._tools.values())
    
    def get_langchain_tools(self):
        """Возвращает инструменты в формате LangChain"""
        return [tool.to_langchain_tool() for tool in self._tools.values()]
    
    def get_tools_description(self) -> str:
        """Форматирует описание всех инструментов для промпта"""
        descriptions = []
        for tool in self._tools.values():
            desc = f"""{tool.name}:
   - Description: {tool.description}
   - Input data: {', '.join([f'{param_name}: {param_type}' for param_name, param_type in tool.args.items()])}"""
            descriptions.append(desc)
        return "\n\n".join(descriptions)
    
