from graph import build_graph
from state import AppState

def lambda_handler(event, context):
    app = build_graph()
    initial_state: AppState = {
        "emails": [],
        "processed_count": 0
    }
    final_state = app.invoke(initial_state)
    return {"status": "success", "processed": final_state.get("processed_count", 0)}

if __name__ == "__main__":
    print(lambda_handler({}, {}))
