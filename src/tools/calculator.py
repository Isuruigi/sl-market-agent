"""Safe calculator tool using AST parsing to prevent code injection"""

import ast
import operator
from typing import Optional


class SafeCalculator:
    """Calculator that prevents code injection using AST parsing"""
    
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def _eval_node(self, node):
        """Evaluate AST node safely.
        
        Args:
            node: AST node to evaluate.
            
        Returns:
            Evaluated result.
            
        Raises:
            ValueError: If unsupported operation is attempted.
        """
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self.OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            return self.OPERATORS[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node).__name__}")
    
    def calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expression.
        
        Args:
            expression: Mathematical expression as string.
            
        Returns:
            Result as string or error message.
        """
        try:
            # Normalize expression
            expr = expression.replace('^', '**').replace('×', '*').replace('÷', '/')
            
            # Parse into AST
            tree = ast.parse(expr, mode='eval')
            
            # Evaluate safely
            result = self._eval_node(tree.body)
            
            # Format result
            if isinstance(result, float):
                return f"Result: {result:.4f}" if result != int(result) else f"Result: {int(result)}"
            return f"Result: {result}"
            
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {str(e)}"


# Create singleton calculator instance
_safe_calc = SafeCalculator()


def evaluate_expression(expression: str) -> str:
    """Safely evaluate a mathematical expression.
    
    Args:
        expression: The mathematical expression to evaluate.
        
    Returns:
        String representation of the result or error message.
    """
    return _safe_calc.calculate(expression)


class CalculatorTool:
    """Legacy wrapper for backwards compatibility."""
    
    def __init__(self):
        """Initialize the calculator tool."""
        self.tool = calculator_tool
        self.calculator = _safe_calc
    
    def calculate(self, expression: str) -> dict:
        """Legacy method for backwards compatibility.
        
        Args:
            expression: Mathematical expression.
            
        Returns:
            Dictionary with result and status.
        """
        result_str = self.calculator.calculate(expression)
        
        if result_str.startswith("Error"):
            return {
                "expression": expression,
                "result": None,
                "status": "error",
                "error": result_str
            }
        else:
            # Extract number from "Result: X"
            try:
                result_value = float(result_str.split(": ")[1])
                return {
                    "expression": expression,
                    "result": result_value,
                    "status": "success"
                }
            except:
                return {
                    "expression": expression,
                    "result": result_str,
                    "status": "success"
                }
    
    def get_tool_description(self) -> dict:
        """Return tool description."""
        return {
            "name": "calculator",
            "description": "Perform mathematical calculations and operations",
            "parameters": {
                "expression": "Mathematical expression to evaluate"
            }
        }


def test_calculator():
    """Test calculator functionality"""
    print("\n" + "="*60)
    print("TESTING CALCULATOR")
    print("="*60 + "\n")
    
    calc = SafeCalculator()
    tests = [
        "2 + 2",
        "100 * 1.05",
        "(250 - 50) / 4",
        "2 ** 10",
        "1 / 0",  # Should handle gracefully
        "-5 + 3",
        "10 - 3 * 2",
    ]
    
    for expr in tests:
        result = calc.calculate(expr)
        print(f"{expr:20s} = {result}")
    
    print("\n" + "="*60)
    print("✅ Calculator test complete")
    print("="*60)


if __name__ == "__main__":
    test_calculator()
