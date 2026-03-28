import socket
import subprocess
import sys
import time

import pytest


def _wait_for_port(port: int, host: str = "127.0.0.1", timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


@pytest.fixture(scope="session")
def live_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not _wait_for_port(8000):
        proc.terminate()
        raise RuntimeError("FastAPI server did not start in time")
    yield "http://127.0.0.1:8000"
    proc.terminate()
    proc.wait()
