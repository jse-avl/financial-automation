import json
import os
import time
from datetime import date

import requests

CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "rates_cache.json",
)


def get_exchange_rates(base="USD"):
    hoy = date.today().isoformat()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            cache = json.load(f)
        if cache.get("date") == hoy:
            return cache["rates"]

    url = f"https://api.frankfurter.dev/v1/latest?base={base}"

    for intento in range(3):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                rates = data["rates"]
                rates[base] = 1.0
                os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump({"date": hoy, "rates": rates}, f, indent=2)
                return rates
        except requests.RequestException:
            if intento < 2:
                time.sleep(2**intento)

    raise ConnectionError(
        "No se pudieron obtener las tasas de cambio después de 3 intentos"
    )
