"""Scoped cleanup and independent reconciliation share the deletion boundary."""
from . import cleanup, monitor


def handler(event, context):
    return cleanup.handler(event, context) if "job" in event else monitor.handler(event, context)
