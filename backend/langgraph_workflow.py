from langgraph.graph import StateGraph

def build_langgraph_workflow():
    graph = StateGraph(dict)
    graph.add_node("generate_itinerary", lambda state: state)
    graph.set_entry_point("generate_itinerary")
    graph.set_finish_point("generate_itinerary")
    return graph.compile()