# tests/utils_net.py
import re, time

API_KEY = "add494e96808c55b3ee7f940c9d5e5b6"

def wait_for_call(driver, path_regex, expected_params=None, timeout=20, subset=True):
    """
    Waits for a request whose path matches `path_regex` and whose query params
    include `expected_params` (subset by default). Always enforces api_key.
    """
    expected_params = expected_params or {}
    expected_params = {**expected_params, "api_key": API_KEY}

    pat = re.compile(path_regex)
    end = time.time() + timeout

    while time.time() < end:
        for req in getattr(driver, "requests", []):
            if not getattr(req, "response", None):
                continue
            if req.path and pat.search(req.path):
                # selenium-wire exposes parsed query in req.params
                qs = dict(req.params or {})
                if _match_params(qs, expected_params, subset=subset):
                    return req
        time.sleep(0.25)

    raise AssertionError(f"Did not find call {path_regex} with params (subset={subset}): {expected_params}")

def _match_params(actual: dict, expected: dict, subset=True) -> bool:
    if subset:
        for k, v in expected.items():
            if str(actual.get(k)) != str(v):
                return False
        return True
    else:
        # exact match
        actual_norm = {k: str(v) for k, v in actual.items()}
        expected_norm = {k: str(v) for k, v in expected.items()}
        return actual_norm == expected_norm
