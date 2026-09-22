import re
import os
from datetime import datetime
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agent.tools import run_linter, run_security_scanner
from agent.prompts import get_review_prompt, get_refactor_prompt

class ReviewState(TypedDict):
    file_path: str
    code_content: str
    linter_output: Optional[str]
    security_output: Optional[str]
    review_output: Optional[str]
    report_path: Optional[str]
    refactored_code: Optional[str]

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1")
model_name = os.getenv("LLM_MODEL", "qwen/qwen3.8-27b")

llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0.2,
)

def clean_think_tag(text: str) -> str:
    """Filters and removes the internal reasoning block <think>...</think> robustly."""
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    if '<think>' in cleaned_text:
        cleaned_text = re.sub(r'<think>.*', '', cleaned_text, flags=re.DOTALL)
        
    return cleaned_text.strip()

def execute_tools_node(state: ReviewState) -> dict:
    """Executes all external system tools and aggregates physical metrics."""
    linter_result = run_linter(state["file_path"])
    security_result = run_security_scanner(state["file_path"])
    
    return {
        "linter_output": linter_result,
        "security_output": security_result
    }

def analyze_code_node(state: ReviewState) -> dict:
    prompt = get_review_prompt(
        file_path=state['file_path'],
        code_content=state['code_content'],
        linter_output=state.get('linter_output', 'No linter data available.'),
        security_output=state.get('security_output', 'No security data available.')
    )
    
    response = llm.invoke(prompt)
    clean_response = clean_think_tag(response.content)
    
    return {"review_output": clean_response}

def save_report_node(state: ReviewState) -> dict:
    """Saves the generated AI review output to a Markdown file."""
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Extract base file name and create a timestamp
    base_name = os.path.basename(state["file_path"])
    file_name_without_ext = os.path.splitext(base_name)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct the final markdown path
    report_filename = f"review_{file_name_without_ext}_{timestamp}.md"
    report_path = os.path.join(reports_dir, report_filename)
    
    # Write the review string directly into the file
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Code Review Report for `{base_name}`\n\n")
        f.write(state.get("review_output", "No output generated."))
        
    return {"report_path": report_path}

def refactor_code_node(state: ReviewState) -> dict:
    """Generates refactored code based on the original code and the AI review."""
    prompt = get_refactor_prompt(
        code_content=state['code_content'],
        review_output=state['review_output']
    )
    
    response = llm.invoke(prompt)
    clean_code = response.content.replace("```python", "").replace("```", "").strip()
    clean_code = clean_think_tag(clean_code)
    
    return {"refactored_code": clean_code}