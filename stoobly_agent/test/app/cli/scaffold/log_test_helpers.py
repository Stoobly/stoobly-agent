import json
from typing import List, Optional


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
