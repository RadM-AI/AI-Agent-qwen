import math
from .base import BaseTool

class CalculatorTool(BaseTool):
    """Инструмент для математических вычислений"""

    @property
    def name(self) -> str:
        return "calculate"
    
    @property
    def description(self) -> str:
        return """Calculate a mathematical expression.
        Args:
            input_data: A mathematical expression (for example: '2 + 2 * 3', 'sin(45)')

        Returns:
            Calculation result
        """

    
    def execute(self, input: str) -> str:
        try:
            print('Начал считать...')
            
            # Безопасный набор разрешенных символов и функций
            allowed_chars = set('0123456789+-*/.() ')
            safe_globals = {
                'sin': math.sin,
                'cos': math.cos, 
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log,
                'log10': math.log10,
                'pi': math.pi,
                'e': math.e
            }
            
            if all(c in allowed_chars for c in input):
                # Безопасное вычисление с ограниченным контекстом
                result = eval(input, {"__builtins__": {}}, safe_globals)
                return f"ОТВЕТ КРАТКИЙ: Результат: {input} = {result}"
            else:
                return "Ошибка: выражение содержит недопустимые символы"
                
        except Exception as e:
            return f"Ошибка вычисления: {str(e)}"