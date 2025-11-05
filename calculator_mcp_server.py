"""
Simple Calculator MCP Server
Demonstrates basic MCP server with four mathematical operations.
"""

from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
# The name "calculator" will be shown in Claude Desktop
mcp = FastMCP("calculator")

import logging
logging.basicConfig(level=logging.INFO)

# Tool 1: Addition
@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers together.

    This tool performs addition of two numbers and returns the sum.

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of a and b

    Examples:
        add(5, 3) -> 8.0
        add(-2, 7) -> 5.0
    """
    logging.info(f"add called with a={a}, b={b}")
    result = a + b
    logging.info(f"add returning {result}")
    return result


# Tool 2: Subtraction
@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Subtract second number from first number.

    This tool performs subtraction: a - b

    Args:
        a: The number to subtract from
        b: The number to subtract

    Returns:
        The difference (a - b)

    Examples:
        subtract(10, 3) -> 7.0
        subtract(5, 8) -> -3.0
    """
    return a - b


# Tool 3: Multiplication
@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    This tool performs multiplication of two numbers.

    Args:
        a: The first number
        b: The second number

    Returns:
        The product of a and b

    Examples:
        multiply(4, 5) -> 20.0
        multiply(-3, 6) -> -18.0
    """
    return a * b


# Tool 4: Division with error handling
@mcp.tool()
async def divide(a: float, b: float) -> dict[str, Any]:
    """Divide first number by second number.

    This tool performs division: a / b
    Includes error handling for division by zero.

    Args:
        a: The dividend (number to be divided)
        b: The divisor (number to divide by)

    Returns:
        Dictionary with result or error message

    Examples:
        divide(10, 2) -> {"success": True, "result": 5.0}
        divide(7, 0) -> {"success": False, "error": "Cannot divide by zero"}
    """
    if b == 0:
        return {
            "success": False,
            "error": "Cannot divide by zero",
        }

    return {
        "success": True,
        "result": a / b,
    }


# Optional: Add a utility tool for help
@mcp.tool()
async def get_capabilities() -> dict[str, Any]:
    """Get information about calculator capabilities.

    Returns:
        Dictionary with available operations and descriptions
    """
    return {
        "server": "Calculator MCP Server",
        "version": "1.0.0",
        "operations": [
            {"name": "add", "description": "Addition of two numbers"},
            {"name": "subtract", "description": "Subtraction of two numbers"},
            {"name": "multiply", "description": "Multiplication of two numbers"},
            {"name": "divide", "description": "Division with zero-check"},
        ],
        "usage": "Ask natural language questions like 'What is 5 + 3?'",
    }


def main():
    """Entry point for the MCP server."""
    # Run the server with stdio transport
    # This means the server communicates via standard input/output
    # Perfect for local Claude Desktop integration
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()