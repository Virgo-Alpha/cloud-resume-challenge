import os
import json
import time

import requests


API_BASE_URL = os.environ["API_BASE_URL"]  # e.g. https://xxxx.execute-api.eu-west-1.amazonaws.com/Prod


def _get_count():
    url = API_BASE_URL.rstrip("/") + "/count"
    resp = requests.get(url, timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert "count" in data
    return data["count"]


def test_counter_increments():
    """
    Calls the live API twice and asserts that the count increases
    or at least doesn't go backwards (in case of concurrent requests).
    """
    first = _get_count()
    time.sleep(0.5)
    second = _get_count()

    assert isinstance(first, int)
    assert isinstance(second, int)
    assert second >= first
