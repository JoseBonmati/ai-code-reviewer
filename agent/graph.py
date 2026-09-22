from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agent.nodes import ReviewState, analyze_code_node, execute_tools_node, save_report_node, refactor_code_node

def build_graph():
    """Constructs and compiles the AI Code Reviewer LangGraph workflow with HITL."""
    workflow = StateGraph(ReviewState)
    
    # Add execution nodes
    workflow.add_node("execute_tools", execute_tools_node)
    workflow.add_node("analyze_code", analyze_code_node)
    workflow.add_node("save_report", save_report_node)
    workflow.add_node("refactor_code", refactor_code_node)
    
    # Define sequential execution flow
    workflow.add_edge(START, "execute_tools")
    workflow.add_edge("execute_tools", "analyze_code")
    workflow.add_edge("analyze_code", "save_report")
    workflow.add_edge("save_report", "refactor_code")
    workflow.add_edge("refactor_code", END)
    
    memory = MemorySaver()

    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["refactor_code"]
    )

# Exported compiled graph instance
graph = build_graph()