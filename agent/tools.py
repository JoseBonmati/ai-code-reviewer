import subprocess

def run_linter(file_path: str) -> str:
    """Executes flake8 on the target file and returns the physical stdout/stderr."""
    try:
        result = subprocess.run(
            ["flake8", file_path, "--max-line-length=100"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.stdout:
            return result.stdout.strip()
        elif result.stderr:
            return f"Linter Execution Error: {result.stderr.strip()}"
        else:
            return "No syntax or styling errors detected by flake8."
            
    except FileNotFoundError:
        return "Error: flake8 is not installed or not found in system PATH."
    except Exception as e:
        return f"Unexpected error executing linter: {str(e)}"

def run_security_scanner(file_path: str) -> str:
    """Executes bandit to detect security vulnerabilities in the target file."""
    try:
        # Run bandit quietly (-q) to only show actual errors, targeting the specific file
        result = subprocess.run(
            ["bandit", "-q", "-r", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.stdout:
            return result.stdout.strip()
        elif result.stderr:
            return f"Scanner Execution Error: {result.stderr.strip()}"
        else:
            return "No security vulnerabilities detected by Bandit."
            
    except FileNotFoundError:
        return "Error: bandit is not installed or not found in system PATH."
    except Exception as e:
        return f"Unexpected error executing security scanner: {str(e)}"