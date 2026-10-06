from mcp_server.server import (
    get_employee,
    get_service,
    get_incident,
)


print(
    get_employee("EMP001")
)

print(
    get_service("PAYMENT-GATEWAY")
)

print(
    get_incident("INC-2025-004")
)