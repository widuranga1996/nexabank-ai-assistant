from app.security.rbac import has_permission

from mcp_server.server import (
    get_employee,
    get_service,
    get_incident,
)


def call_mcp_tool(
    user_id: str,
    tool_name: str,
    argument: str,
) -> dict:

    if not has_permission(
        user_id,
        "mcp",
    ):
        return {
            "error": "Permission denied",
            "tool": tool_name,
        }

    if tool_name == "get_employee":

        return get_employee(argument)

    if tool_name == "get_service":

        return get_service(argument)

    if tool_name == "get_incident":

        return get_incident(argument)

    return {
        "error": "Unknown MCP tool"
    }