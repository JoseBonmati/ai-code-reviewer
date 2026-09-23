from agent.nodes import clean_think_tag

def test_clean_think_tag_no_tags():
    """Verifies that standard LLM output without reasoning tags is unmodified."""
    text = "Here is the refactored code:\n```python\nprint('Hello')\n```"
    result = clean_think_tag(text)
    assert result == text

def test_clean_think_tag_multiline():
    """Verifies that multiline <think> blocks (DeepSeek/Qwen style) are removed."""
    text = """<think>
    I need to check for SQL injection first.
    The user is not using parameterized queries.
    </think>
    Here is the security report."""
    
    expected = "\n    Here is the security report."
    result = clean_think_tag(text)
    assert result.strip() == expected.strip()

def test_clean_think_tag_single_line():
    """Verifies that single-line inline <think> tags are cleanly stripped."""
    text = "<think>Refactoring now...</think>Final output."
    expected = "Final output."
    result = clean_think_tag(text)
    assert result.strip() == expected.strip()