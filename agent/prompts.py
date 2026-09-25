def get_review_prompt(file_path: str, code_content: str, linter_output: str, security_output: str) -> str:
    return f"""You are a Senior Code Reviewer. Be highly concise and direct.
Analyze the following code alongside its physical execution metrics.
Generate a brief response structured strictly into:
- **Bugs or Security Vulnerabilities**
- **Performance Optimizations**
- **Readability and Cleanliness**

CRITICAL INSTRUCTIONS: 
Keep your internal reasoning as short as possible. Output ONLY the requested sections with brief bullet points.
Use the provided Linter (flake8) and Security (bandit) outputs as factual grounding.

Code to review ({file_path}):
---
{code_content}
---

Physical Linter Output (flake8):
---
{linter_output}
---

Physical Security Scanner Output (bandit):
---
{security_output}
---
"""

def get_refactor_prompt(code_content: str, review_output: str) -> str:
    return f"""You are an Expert Python Developer.
Your task is to refactor the following code based ONLY on the provided code review.
Do not add new features, just fix the bugs, optimize performance, and clean the code as suggested.

CRITICAL INSTRUCTIONS:
Output ONLY the raw Python code. Do not include markdown formatting like ```python.
Do not include any explanations.

CRITICAL COMMENTING RULES:
- DO NOT output your internal reasoning, decision-making process, or monologues as Python comments.
- Code comments must be STRICTLY limited to standard professional docstrings and essential technical explanations.
- Never use conversational phrases like "Let's assume", "Actually", "For the purpose of this refactor", or "I will use". Write confident, production-ready code.

Original Code:
---
{code_content}
---

Code Review Report:
---
{review_output}
---
"""