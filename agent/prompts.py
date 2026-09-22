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

Original Code:
---
{code_content}
---

Code Review Report:
---
{review_output}
---
"""