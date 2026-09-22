import os
import shutil
import uuid
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import graph

app = FastAPI(title="AI Code Reviewer API", version="4.0")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"

# Outline for retrieving the thread ID from the frontend
class RefactorRequest(BaseModel):
    thread_id: str

@app.post("/api/review")
async def review_code(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py files are supported.")
    
    # Ensure the data/ directory exists and save the uploaded file
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    # Read the content for the AI
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

    # Prepare the initial state
    initial_state = {
        "file_path": file_path,
        "code_content": code_content,
        "linter_output": None,
        "security_output": None,
        "review_output": None,
        "report_path": None,
        "refactored_code": None
    }
    
    # Generate a unique ID for the LangGraph memory
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Pass the config. The graph will pause after saving the report.
        result = graph.invoke(initial_state, config)
        return {
            "status": "success",
            "file_analyzed": file.filename,
            "report_path": result.get("report_path"),
            "review": result.get("review_output", "No review generated."),
            "original_code": code_content,
            "thread_id": thread_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent execution error: {e}")

@app.post("/api/refactor")
async def refactor_code(request: RefactorRequest):
    """Resume execution of the paused graph to generate the corrected code."""
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        # Pass None as the initial state to indicate that it should continue from where it left off
        result = graph.invoke(None, config)
        return {
            "status": "success",
            "refactored_code": result.get("refactored_code", "No code generated.")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent refactor error: {e}")

if __name__ == "__main__":
    print("Starting AI Code Reviewer Backend on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)