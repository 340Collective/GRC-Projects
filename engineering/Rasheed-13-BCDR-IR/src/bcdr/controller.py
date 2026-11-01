"""Restore controller and result publisher. No source-data write permissions."""
from . import restore, report


def handler(event, context):
    return restore.handler(event, context) if event.get("action") not in {None, "report"} else report.handler(event, context)
