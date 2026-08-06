from fastmcp import FastMCP

mcp = FastMCP("ASB Campaigns MCP")

# --- TOOLS: actions an agent can call ---
@mcp.tool
def echo(original_string: str) -> str:
    """Returns the same text provided as input."""
    return f"Echo: {original_string}"


if __name__ == "__main__":
    # HTTP transport: the server listens on http://127.0.0.1:8000/mcp
    mcp.run(transport="http", host="127.0.0.1", port=8000)