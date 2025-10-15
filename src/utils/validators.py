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
    
    dangerous_keywords = ['import', 'exec', 'eval', '__', 'open', 'file', 'os', 'sys']
    expr_lower = expr.lower()
    
    # Проверка на опасные ключевые слова
    if any(keyword in expr_lower for keyword in dangerous_keywords):
        return False
    
    # Проверка на допустимые символы и функции
    allowed_chars = set('0123456789+-*/.() ')
    allowed_functions = ['sin', 'cos', 'tan', 'sqrt', 'log', 'log10', 'pi', 'e']
    
    # Упрощенная проверка - в реальном проекте нужен парсер
    return all(c in allowed_chars for c in expr.replace(' ', ''))