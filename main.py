import os
import sys
from agent.graph import graph

def main():
    # Check whether a file has been passed as an argument in the terminal
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Safety fallback to the test file
        file_path = "data/sample.py"
        print(f"No file provided. Using default: {file_path}")
        print(f"Tip: You can pass a file like this: python main.py path/to/your/file.py\n")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    print(f"Reading code from: {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()
        
    # Prepare the initial state dictionary
    initial_state = {
        "file_path": file_path,
        "code_content": code_content,
        "linter_output": None,
        "security_output": None,
        "review_output": None,
        "report_path": None
    }
    
    print("The agent is analyzing the code. Please wait...\n")
    
    try:
        # Trigger the LangGraph execution
        result = graph.invoke(initial_state)
        
        print("=" * 60)
        print("AI CODE REVIEW RESULTS")
        print("=" * 60)
        print(result.get("review_output", "No output generated."))
        print("=" * 60)
        
        if "report_path" in result:
            print(f"\nReport successfully saved to: {result['report_path']}")
            
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()