import os
import sys
from agent.graph import graph

def process_file(file_path: str):
    """Reads a file and triggers the LangGraph review pipeline."""
    print(f"\nReading code from: {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Prepare the initial state dictionary
    initial_state = {
        "file_path": file_path,
        "code_content": code_content,
        "linter_output": None,
        "security_output": None,
        "review_output": None,
        "report_path": None
    }
    
    print(f"The agent is analyzing '{os.path.basename(file_path)}'. Please wait...")
    
    try:
        # Trigger the LangGraph execution
        result = graph.invoke(initial_state)
        
        if "report_path" in result:
            print(f"Report successfully saved to: {result['report_path']}")
            
    except Exception as e:
        print(f"Error during execution for {file_path}: {e}")

def main():
    target_path = "data/"
    
    print("Initializing AI Code Reviewer...")
    
    # Check if the directory exists
    if not os.path.exists(target_path):
        print(f"Error: Directory '{target_path}' not found.")
        sys.exit(1)
        
    print(f"Scanning secure directory: {target_path}")
    
    files_processed = 0
    # Recursively find and process all .py files
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                process_file(full_path)
                files_processed += 1
                
    if files_processed == 0:
        print(f"No Python files found in '{target_path}'.")

if __name__ == "__main__":
    main()