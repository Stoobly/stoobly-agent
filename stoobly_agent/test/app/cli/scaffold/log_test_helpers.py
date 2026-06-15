import json
import requests
import time
from typing import List

from stoobly_agent.app.proxy.constants.custom_response_codes import NOT_FOUND


def wait_for_forward_proxy_intercept(proxy_url: str, hostname: str, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """Poll until the forward proxy returns 499 for unrecorded requests, confirming intercept mode is active."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(
                f'http://{hostname}/',
                proxies={'http': proxy_url, 'https': proxy_url},
                verify=False,
                timeout=5.0,
            )
            if resp.status_code == NOT_FOUND:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False


def find_all_log_entries(output: str, filters: dict = None) -> List[dict]:
    """Parse NDJSON output and return all entries matching optional filters (AND logic)."""
    results = []
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if filters:
            if not all(entry.get(k) == v for k, v in filters.items()):
                continue
        results.append(entry)
    return results


def count_log_entries(output: str) -> int:
    return len(find_all_log_entries(output))
