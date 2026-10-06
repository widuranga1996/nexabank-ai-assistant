from mcp.server.mcpserver import MCPServer


mcp = MCPServer(
    name="NexaBank Enterprise Data"
)


EMPLOYEES = {
    "EMP001": {
        "employee_id": "EMP001",
        "name": "John Smith",
        "department": "Finance",
        "role": "Finance Analyst",
    },
    "EMP002": {
        "employee_id": "EMP002",
        "name": "Sarah Perera",
        "department": "Payments",
        "role": "Operations Manager",
    },
}


SERVICES = {
    "PAYMENT-GATEWAY": {
        "service_id": "PAYMENT-GATEWAY",
        "name": "Payment Gateway",
        "owner": "Payments Platform",
        "criticality": "HIGH",
        "status": "OPERATIONAL",
    },
    "CUSTOMER-API": {
        "service_id": "CUSTOMER-API",
        "name": "Customer API",
        "owner": "Customer Platform",
        "criticality": "HIGH",
        "status": "OPERATIONAL",
    },
}


INCIDENTS = {
    "INC-2025-004": {
        "incident_id": "INC-2025-004",
        "service": "PAYMENT-GATEWAY",
        "severity": "HIGH",
        "status": "RESOLVED",
        "root_cause": "Database connection pool exhaustion",
    },
    "INC-2025-007": {
        "incident_id": "INC-2025-007",
        "service": "PAYMENT-GATEWAY",
        "severity": "MEDIUM",
        "status": "RESOLVED",
        "root_cause": "External gateway latency",
    },
}


@mcp.tool()
def get_employee(employee_id: str) -> dict:

    employee = EMPLOYEES.get(employee_id)

    if not employee:
        return {
            "error": "Employee not found"
        }

    return employee


@mcp.tool()
def get_service(service_id: str) -> dict:

    service = SERVICES.get(service_id)

    if not service:
        return {
            "error": "Service not found"
        }

    return service


@mcp.tool()
def get_incident(incident_id: str) -> dict:

    incident = INCIDENTS.get(incident_id)

    if not incident:
        return {
            "error": "Incident not found"
        }

    return incident