import os, logging
from graph import build_graph

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = build_graph()

def lambda_handler(event, context):
    # allow overriding fetch count via event
    initial_state = {"MAX_FETCH": int(event.get("max_fetch", os.getenv("MAX_FETCH", 10)))}
    try:
        final = app.invoke(initial_state)
        logger.info("Workflow finished")
        return {"status":"ok","processed": len(final.get("emails",[]))}
    except Exception as e:
        logger.exception("Workflow error")
        raise
