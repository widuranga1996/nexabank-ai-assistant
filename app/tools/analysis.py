from collections import Counter


def analyze_incident_batch(incidents: list[dict]) -> dict:
    """
    Deterministic analysis of a batch of incident records.

    The LLM identifies and organizes the research problem,
    while Python performs reliable aggregation.
    """

    root_causes = Counter()

    for incident in incidents:
        cause = incident.get("root_cause")

        if cause:
            root_causes[cause] += 1

    return {
        "incident_count": len(incidents),
        "root_causes": dict(root_causes),
    }


def aggregate_batch_results(results: list[dict]) -> dict:
    """
    Aggregate results produced by recursive batch analysis.
    """

    total_incidents = 0
    root_causes = Counter()

    for result in results:
        total_incidents += result.get(
            "incident_count",
            0,
        )

        for cause, count in result.get(
            "root_causes",
            {},
        ).items():

            root_causes[cause] += count

    return {
        "total_incidents": total_incidents,
        "root_causes": dict(root_causes),
    }