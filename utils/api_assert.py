import re, time

def wait_for_call(driver, path_regex, expected_params=None, timeout=10):
    end = time.time() + timeout
    pattern = re.compile(path_regex)
    expected_params = expected_params or {}

    while time.time() < end:
        for req in getattr(driver, "requests", []):
            if req.response and req.url and pattern.search(req.path):
                ok = all(str(req.params.get(k)) == str(v) for k, v in expected_params.items())
                if ok:
                    return req
        time.sleep(0.25)
    raise AssertionError(f"Did not observe API call matching {path_regex} with params {expected_params}")
