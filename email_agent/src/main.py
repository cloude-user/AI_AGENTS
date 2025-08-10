import os
import logging
from graph import build_graph

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = build_graph()

def lambda_handler(event, context):
    initial_state = {"MAX_FETCH": int(event.get("max_fetch", os.getenv("MAX_FETCH", 10)))}
    try:
        final = app.invoke(initial_state)
        processed = len(final.get("emails") or [])
        logger.info("Workflow finished")
        return {"status": "ok", "processed": processed}
    except Exception as e:
        logger.exception("Workflow error")
        return {"statusCode": 500, "body": str(e)}