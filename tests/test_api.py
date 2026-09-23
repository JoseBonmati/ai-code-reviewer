import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

# Initialize the FastAPI test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_dummy_files():
    """Automatically removes dummy files created during tests."""
    yield  # Allows the test to run and finish
    
    # Cleanup phase
    dummy_path = os.path.join("data", "dummy.py")
    if os.path.exists(dummy_path):
        os.remove(dummy_path)

def test_review_rejects_non_python_files():
    """Ensures the API blocks any file that does not have a .py extension."""
    # Simulate uploading a .txt file
    files = {"file": ("test.txt", b"print('Hello')", "text/plain")}
    response = client.post("/api/review", files=files)
    
    assert response.status_code == 400
    assert "Only .py files are supported" in response.json()["detail"]

@patch("main.graph.invoke")
def test_review_accepts_python_files(mock_invoke):
    """Tests a successful Python file upload, mocking the LangGraph execution."""
    # Define the fake response the graph should return
    mock_invoke.return_value = {
        "report_path": "reports/mock_report.md",
        "review_output": "Mocked AI Review Output"
    }
    
    # Simulate the file upload
    file_content = b"def test():\n    pass"
    files = {"file": ("dummy.py", file_content, "text/x-python")}
    
    response = client.post("/api/review", files=files)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert data["file_analyzed"] == "dummy.py"
    assert data["review"] == "Mocked AI Review Output"
    assert data["original_code"] == "def test():\n    pass"
    assert "thread_id" in data  # Ensure UUID is generated
    
    # Ensure LangGraph was actually called during the request
    mock_invoke.assert_called_once()

@patch("main.graph.invoke")
def test_refactor_endpoint(mock_invoke):
    """Tests the HITL resume endpoint for code refactoring."""
    # Define the fake refactored code
    mock_invoke.return_value = {
        "refactored_code": "def test():\n    print('Fixed!')"
    }
    
    # Simulate the frontend sending the thread_id
    payload = {"thread_id": "123e4567-e89b-12d3-a456-426614174000"}
    response = client.post("/api/refactor", json=payload)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert data["refactored_code"] == "def test():\n    print('Fixed!')"
    
    mock_invoke.assert_called_once()