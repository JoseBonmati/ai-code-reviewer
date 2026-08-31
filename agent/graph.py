from langgraph.graph import StateGraph, START, END
from agent.nodes import ReviewState, analyze_code_node, execute_tools_node

def build_graph():
    """Constructs and compiles the AI Code Reviewer LangGraph workflow."""
    workflow = StateGraph(ReviewState)
    
    # Add execution nodes
    workflow.add_node("execute_tools", execute_tools_node)
    workflow.add_node("analyze_code", analyze_code_node)
    
    # Define sequential execution flow
    workflow.add_edge(START, "execute_tools")
    workflow.add_edge("execute_tools", "analyze_code")
    workflow.add_edge("analyze_code", END)
    
    # Compile execution pipeline
    return workflow.compile()

# Exported compiled graph instance
graph = build_graph()