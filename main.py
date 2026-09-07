import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent.graph import graph

app = FastAPI(title="AI Code Reviewer API", version="2.0")

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"

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

    # Prepare the initial state and trigger LangGraph
    initial_state = {
        "file_path": file_path,
        "code_content": code_content,
        "linter_output": None,
        "security_output": None,
        "review_output": None,
        "report_path": None
    }
    
    try:
        result = graph.invoke(initial_state)
        return {
            "status": "success",
            "file_analyzed": file.filename,
            "report_path": result.get("report_path"),
            "review": result.get("review_output", "No review generated.")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent execution error: {e}")

if __name__ == "__main__":
    print("Starting AI Code Reviewer Backend on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)