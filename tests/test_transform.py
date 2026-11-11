from datetime import date, timedelta

import pandas as pd

from src.transform import calcular_aging, calcular_metricas, convertir_moneda

RATES = {"USD": 1.0, "EUR": 0.5}


def test_convertir_moneda_divides_by_rate():
    df = pd.DataFrame({"monto": [100.0, 100.0], "moneda": ["USD", "EUR"]})
    out = convertir_moneda(df, RATES)
    assert list(out["monto_usd"]) == [100.0, 200.0]


def test_convertir_moneda_does_not_mutate_input():
    df = pd.DataFrame({"monto": [10.0], "moneda": ["USD"]})
    convertir_moneda(df, RATES)
    assert "monto_usd" not in df.columns


def _aging_for(days_overdue):
    due = pd.Timestamp(date.today() - timedelta(days=days_overdue))
    df = pd.DataFrame({"fecha_vencimiento": [due]})
    return calcular_aging(df).iloc[0]["aging"]


def test_aging_buckets():
    assert _aging_for(-5) == "Al día"
    assert _aging_for(0) == "Al día"
    assert _aging_for(1) == "0-30 días"
    assert _aging_for(30) == "0-30 días"
    assert _aging_for(31) == "31-60 días"
    assert _aging_for(60) == "31-60 días"
    assert _aging_for(61) == "61-90 días"
    assert _aging_for(90) == "61-90 días"
    assert _aging_for(91) == "+90 días"


def test_calcular_metricas():
    df = pd.DataFrame(
        {"tipo": ["CxC", "CxC", "CxP"], "monto_usd": [100.0, 50.0, 30.0]}
    )
    assert calcular_metricas(df) == {
        "total_cxc_usd": 150.0,
        "total_cxp_usd": 30.0,
        "flujo_neto_usd": 120.0,
    }
