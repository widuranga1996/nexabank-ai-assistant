from app.tools.mcp_tools import call_mcp_tool


tests = [
    (
        "user001",
        "get_employee",
        "EMP001",
    ),
    (
        "user002",
        "get_employee",
        "EMP001",
    ),
    (
        "user002",
        "get_incident",
        "INC-2025-004",
    ),
    (
        "admin001",
        "get_incident",
        "INC-2025-004",
    ),
]


for user_id, tool_name, argument in tests:

    result = call_mcp_tool(
        user_id=user_id,
        tool_name=tool_name,
        argument=argument,
    )

    print("\n" + "=" * 60)

    print(
        f"User: {user_id}"
    )

    print(
        f"Tool: {tool_name}"
    )

    print(
        f"Argument: {argument}"
    )

    print(
        f"Result: {result}"
    )