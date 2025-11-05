# Hands-on Lab: Building "Calculator" MCP Server 

### System Requirements:
- **Python 3.10 or higher**
- **uv** package manager
- **Claude Desktop** (latest version)

### Update Claude Desktop Configuration

**Location of config file:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Open the config file:**

```bash
# macOS
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
or

Claude Desktop App Menu Settings/Developer click on Edit Config

**Add your server configuration:**

```json
{
  "mcpServers": {
    "calculator": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/lev.plotkin-ext@gong.io/dev/Week-3-Building-an-MCP-Server",
        "run",
        "calculator_mcp_server.py"
      ]
    }
  }
}
```


### Restart Claude Desktop


### Verify Server Connection

1. **Open Claude Desktop**

2. Claude Desktop App Menu Settings/Connectors

3. Should see "calculator" server listed
4. Click on Configure
   - Should see 5 tools:
     - add
     - subtract
     - multiply
     - divide
     - get_capabilities



### Test with Natural Language

Try these queries in Claude Desktop:

**Basic Operations:**
```
1. What is 15 + 27?

2. Calculate 100 minus 37

3. Multiply 8 by 12

4. What's 144 divided by 12?
```

**Error Handling:**
```
5. Divide 10 by 0
   (Should handle gracefully with error message)
```

**Complex Queries:**
```
6. If I have 3 boxes with 24 items each, how many items total?

7. Calculate (50 + 30) * 2

8. What are the calculator's capabilities?
```



## Troubleshooting

### Tools Icon Not Appearing

**1. Check server logs:**
```bash
# View Claude Desktop logs
# macOS:
tail -f ~/Library/Logs/Claude/mcp*.log

# Look for error messages about your calculator server
```

**2. Test server directly:**
```bash
cd calculator-mcp
uv run calculator.py

# Server should start and wait for input
# Press Ctrl+C to exit
```

**3. Validate JSON config:**
```bash
# macOS
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Should print formatted JSON without errors
```



**View logs in Claude Desktop:**
Menu in Claude Desktop App: Help->Troubleshooting-> Show Logs in Finder
- Logs show tool invocations and responses
- Help debug issues

---

## 🎓 Understanding Your Server

### Server Architecture:

```
Your calculator-mcp Server:

┌──────────────────────────────────┐
│     FastMCP Framework            │
│  (Handles protocol complexity)   │
└────────────┬─────────────────────┘
             │
    ┌────────┴────────┐
    │   Transport     │
    │   (stdio)       │
    └────────┬────────┘
             │ JSON-RPC 2.0
             │
    ┌────────┴────────┐
    │  Tool Registry  │
    │  • add          │
    │  • subtract     │
    │  • multiply     │
    │  • divide       │
    │  • capabilities │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │ Request Handler │
    │ • tools/list    │
    │ • tools/call    │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │  Your Code!     │
    │  (business      │
    │   logic)        │
    └─────────────────┘
```

### Message Flow Example:

**Claude: "What is 5 + 3?"**

```json
// 1. Claude → Server: List available tools
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}

// 2. Server → Claude: Here are my tools
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "add",
        "description": "Add two numbers together...",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
          },
          "required": ["a", "b"]
        }
      }
      // ... other tools
    ]
  }
}

// 3. Claude → Server: Call the add tool
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "add",
    "arguments": {
      "a": 5,
      "b": 3
    }
  }
}

// 4. Server → Claude: Here's the result
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "8.0"
      }
    ]
  }
}

// 5. Claude → User: "The sum of 5 and 3 is 8"
```

---

## 🚀 Extension Challenges

Now that you have a working server, try these extensions:

### Challenge 1: Add More Operations (Easy)
```python
@mcp.tool()
async def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent"""
    return base ** exponent

@mcp.tool()
async def square_root(n: float) -> dict[str, Any]:
    """Calculate square root of a number"""
    if n < 0:
        return {"success": False, "error": "Cannot calculate square root of negative number"}
    return {"success": True, "result": n ** 0.5}
```

### Challenge 2: Add Resources (Medium)
```python
@mcp.resource("calculator://history")
async def get_calculation_history() -> str:
    """Return history of calculations performed"""
    # Implement calculation tracking
    return "Recent calculations:\n1. add(5, 3) = 8\n..."
```

### Challenge 3: Add Error Handling (Medium)
```python
from functools import wraps

def handle_calculation_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            return {"success": False, "error": f"Invalid input: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}"}
    return wrapper

@mcp.tool()
@handle_calculation_errors
async def divide(a: float, b: float) -> dict[str, Any]:
    # ...
```

### Challenge 4: Add Validation (Advanced)
```python
@mcp.tool()
async def factorial(n: int) -> dict[str, Any]:
    """Calculate factorial of a non-negative integer"""
    if not isinstance(n, int):
        return {"success": False, "error": "Input must be an integer"}
    if n < 0:
        return {"success": False, "error": "Factorial undefined for negative numbers"}
    if n > 170:
        return {"success": False, "error": "Result too large (overflow)"}
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return {"success": True, "result": result}
```

---

## 📚 Key Takeaways

1. ✅ **MCP Server = Tools + Communication Protocol**
   - Tools are just Python functions with decorators
   - Protocol (JSON-RPC) is handled by FastMCP

2. ✅ **Type Hints = Automatic Schema**
   - Python types → JSON Schema
   - No manual schema writing needed

3. ✅ **Docstrings = Tool Documentation**
   - Claude reads your docstrings
   - Good docs = Better AI understanding

4. ✅ **STDIO Transport = Easy Local Integration**
   - No server setup needed
   - Claude Desktop manages process

5. ✅ **Error Handling = Better UX**
   - Return structured error messages
   - Claude can explain errors to users

---
