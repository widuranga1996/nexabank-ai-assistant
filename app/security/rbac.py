USERS = {
    "user001": {
        "username": "user001",
        "role": "Viewer",
    },
    "user002": {
        "username": "user002",
        "role": "Analyst",
    },
    "admin001": {
        "username": "admin001",
        "role": "Administrator",
    },
}


ROLE_PERMISSIONS = {
    "Viewer": {
        "chat",
        "knowledge_search",
    },

    "Analyst": {
        "chat",
        "knowledge_search",
        "analytics",
        "mcp",
        "python_analysis",
    },

    "Administrator": {
        "chat",
        "knowledge_search",
        "analytics",
        "mcp",
        "python_analysis",
        "restricted_documents",
        "administration",
    },
}


def get_user(user_id: str):

    return USERS.get(user_id)


def get_role(user_id: str):

    user = get_user(user_id)

    if not user:
        return None

    return user["role"]


def has_permission(
    user_id: str,
    permission: str,
) -> bool:

    role = get_role(user_id)

    if not role:
        return False

    return permission in ROLE_PERMISSIONS.get(
        role,
        set(),
    )