async def analyze_incidents(incidents):

    root_causes = {}

    for incident in incidents:
        cause = incident["root_cause"]

        root_causes[cause] = (
            root_causes.get(cause, 0) + 1
        )

    return {
        "total_incidents": len(incidents),
        "root_causes": root_causes,
    }