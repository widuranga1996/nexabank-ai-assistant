from app.security.rbac import get_role


SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "reveal confidential",
    "show me confidential",
    "bypass security",
    "disable security",
    "give me administrator documents",
]


def detect_prompt_injection(
    query: str,
) -> list[str]:

    query_lower = query.lower()

    flags = []

    for pattern in SUSPICIOUS_PATTERNS:

        if pattern in query_lower:

            flags.append(
                f"Prompt injection pattern detected: {pattern}"
            )

    return flags


def security_check(
    user_id: str,
    query: str,
) -> dict:

    flags = detect_prompt_injection(query)

    role = get_role(user_id)

    if not role:

        flags.append(
            "Unknown user."
        )

    return {
        "allowed": len(flags) == 0,
        "role": role,
        "flags": flags,
    }