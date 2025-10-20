import os  # Required for path operations

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

# Import prompt from separate file for better organization
from .prompts import GET_TO_KNOW_ME_INSTRUCTION

get_to_know_me = LlmAgent(
    name="get_to_know_me",
    model="gemini-2.5-flash",
    description="Get to know the user agent",
    instruction=GET_TO_KNOW_ME_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",  # Argument for npx to auto-confirm install
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                        # npx process can access.
                        # Replace with a valid absolute path on your system.
                        # For example: "/Users/youruser/accessible_mcp_files"
                        # or use a dynamically constructed absolute path:
                        os.path.abspath("ROOT_PATH_TO_READ"),
                    ],
                ),
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # Recommended for "get to know me" use case - only expose read/write capabilities
            tool_filter=[
                "list_directory",
                "read_file",
                "write_file",
                "create_directory",
            ],
        )
    ],
)

root_agent = get_to_know_me
