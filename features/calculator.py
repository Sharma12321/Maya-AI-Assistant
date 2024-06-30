import math

class Calculator:
    def calculate(self, expression):
        try:
            # Use a whitelist of safe mathematical functions
            safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith('__')}
            safe_dict.update({
                'abs': abs,
                'round': round,
                'max': max,
                'min': min
            })
            result = eval(expression, {"__builtins__": None}, safe_dict)
            return f"The result is {result}"
        except Exception as e:
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"