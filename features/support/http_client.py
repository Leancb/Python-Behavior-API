import os
import time
import json
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))
BASE_URL = os.getenv("BASE_URL", "https://reqres.in")
REQRES_API_KEY = os.getenv("REQRES_API_KEY", "").strip()
REQRES_BEARER = os.getenv("REQRES_BEARER", "").strip()

class ResponseWrapper:
    def __init__(self, response: requests.Response, elapsed_ms: int):
        self.response = response
        self.elapsed_ms = elapsed_ms

def _merge_url(path: str) -> str:
    if path.startswith("http"):
        return path
    return BASE_URL.rstrip("/") + "/" + path.lstrip("/")

def _default_headers() -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if REQRES_API_KEY:
        headers["x-api-key"] = REQRES_API_KEY
    if REQRES_BEARER:
        headers["Authorization"] = f"Bearer {REQRES_BEARER}"
    return headers

def request(method: str, path: str, body: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> ResponseWrapper:
    url = _merge_url(path)
    merged = _default_headers()
    if headers:
        merged.update(headers)
    data = json.dumps(body) if isinstance(body, dict) else body

    start = time.perf_counter_ns()
    resp = requests.request(method=method.upper(), url=url, data=data,
                            headers=merged, timeout=DEFAULT_TIMEOUT)
    elapsed_ms = int((time.perf_counter_ns() - start) / 1_000_000)
    return ResponseWrapper(resp, elapsed_ms)
