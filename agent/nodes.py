import re
import os
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

class ReviewState(TypedDict):
    file_path: str
    code_content: str
    review_output: Optional[str]

load_dotenv()

# Fetch configuration from environment variables with fallbacks
api_key = os.getenv("API_KEY")
base_url = os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1")
model_name = os.getenv("LLM_MODEL", "qwen/qwen3.6-27b")

llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model=model_name,
    temperature=0.2
)

def clean_think_tag(text: str) -> str:
    """Filters and removes the internal reasoning block <think>...</think> robustly."""
    # Remove everything between <think> and </think>
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Fallback: If </think> is missing due to generation limits, remove from <think> to the end
    if '<think>' in cleaned_text:
        cleaned_text = re.sub(r'<think>.*', '', cleaned_text, flags=re.DOTALL)
        
    return cleaned_text.strip()

def analyze_code_node(state: ReviewState) -> dict:
    prompt = f"""You are a Senior Code Reviewer. Be highly concise and direct.
Analyze the following code and generate a brief response structured strictly into:
- **Bugs or Security Vulnerabilities**
- **Performance Optimizations**
- **Readability and Cleanliness**

CRITICAL INSTRUCTIONS: 
Keep your internal reasoning as short as possible. Output ONLY the requested sections with brief bullet points. Do not write long explanations.

Code to review ({state['file_path']}):

{state['code_content']}

"""
    response = llm.invoke(prompt)
    clean_response = clean_think_tag(response.content)
    
    return {"review_output": clean_response}