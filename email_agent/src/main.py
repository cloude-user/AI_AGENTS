from graph import build_graph

def lambda_handler(event, context):
    workflow = build_graph()
    final_state = workflow.invoke({})
    return {"status": "done", "processed": len(final_state.emails)}
