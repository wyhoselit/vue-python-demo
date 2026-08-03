from typing import Any, Dict, List, Union

SENSITIVE_KEYS = {"password", "hashed_password", "access_token", "api_key", "secret"}

def redact_sensitive_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            k: "[REDACTED]" if k.lower() in SENSITIVE_KEYS else redact_sensitive_data(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    return data
