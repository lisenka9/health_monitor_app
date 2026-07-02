import subprocess
import json

def test_schemathesis():
    result = subprocess.run(
        ["schemathesis", "run", "http://localhost:8000/openapi.json", "--checks", "all", "--json"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Schemathesis failed: {result.stderr}"