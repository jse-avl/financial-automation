import json
from datetime import date

import pytest
import requests

from src import fetch_rates


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


@pytest.fixture(autouse=True)
def isolated_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_rates, "CACHE_FILE", str(tmp_path / "cache.json"))
    monkeypatch.setattr(fetch_rates.time, "sleep", lambda _s: None)
    return tmp_path / "cache.json"


def test_fetches_and_caches_rates(monkeypatch, isolated_cache):
    monkeypatch.setattr(
        fetch_rates.requests,
        "get",
        lambda *a, **k: FakeResponse(200, {"rates": {"EUR": 0.9}}),
    )
    rates = fetch_rates.get_exchange_rates("USD")
    assert rates == {"EUR": 0.9, "USD": 1.0}
    cached = json.loads(isolated_cache.read_text(encoding="utf-8"))
    assert cached["date"] == date.today().isoformat()
    assert cached["rates"] == rates


def test_uses_todays_cache_without_network(monkeypatch, isolated_cache):
    isolated_cache.write_text(
        json.dumps({"date": date.today().isoformat(), "rates": {"USD": 1.0, "EUR": 0.8}}),
        encoding="utf-8",
    )

    def boom(*a, **k):
        raise AssertionError("no debería llamar a la red")

    monkeypatch.setattr(fetch_rates.requests, "get", boom)
    assert fetch_rates.get_exchange_rates("USD")["EUR"] == 0.8


def test_stale_cache_is_refreshed(monkeypatch, isolated_cache):
    isolated_cache.write_text(
        json.dumps({"date": "2000-01-01", "rates": {"USD": 1.0, "EUR": 0.1}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        fetch_rates.requests,
        "get",
        lambda *a, **k: FakeResponse(200, {"rates": {"EUR": 0.9}}),
    )
    assert fetch_rates.get_exchange_rates("USD")["EUR"] == 0.9


def test_retries_then_succeeds(monkeypatch):
    calls = {"n": 0}

    def flaky(*a, **k):
        calls["n"] += 1
        if calls["n"] < 3:
            raise requests.ConnectionError("down")
        return FakeResponse(200, {"rates": {"EUR": 0.9}})

    monkeypatch.setattr(fetch_rates.requests, "get", flaky)
    assert fetch_rates.get_exchange_rates("USD")["EUR"] == 0.9
    assert calls["n"] == 3


def test_raises_after_three_failed_attempts(monkeypatch):
    calls = {"n": 0}

    def always_fail(*a, **k):
        calls["n"] += 1
        raise requests.Timeout("slow")

    monkeypatch.setattr(fetch_rates.requests, "get", always_fail)
    with pytest.raises(ConnectionError):
        fetch_rates.get_exchange_rates("USD")
    assert calls["n"] == 3


def test_non_200_status_counts_as_failure(monkeypatch):
    monkeypatch.setattr(
        fetch_rates.requests, "get", lambda *a, **k: FakeResponse(500)
    )
    with pytest.raises(ConnectionError):
        fetch_rates.get_exchange_rates("USD")
