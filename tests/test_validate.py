import pandas as pd

from src.validate import validate_dataframe

RATES = {"USD": 1.0, "EUR": 0.9}


def _row(**overrides):
    base = {
        "id": 1,
        "tipo": "CxC",
        "cliente_proveedor": "ACME",
        "moneda": "USD",
        "monto": 100.0,
        "fecha_emision": "2026-01-01",
        "fecha_vencimiento": "2026-02-01",
    }
    base.update(overrides)
    return base


def _validate(*rows):
    return validate_dataframe(pd.DataFrame(list(rows)), RATES)


def test_valid_row_passes():
    clean, errors = _validate(_row())
    assert len(clean) == 1
    assert errors.empty


def test_negative_amount_rejected():
    clean, errors = _validate(_row(monto=-5))
    assert clean.empty
    assert errors.iloc[0]["campo"] == "monto"


def test_zero_amount_rejected():
    clean, _ = _validate(_row(monto=0))
    assert clean.empty


def test_non_numeric_amount_rejected():
    clean, errors = _validate(_row(monto="abc"))
    assert clean.empty
    assert "número" in errors.iloc[0]["motivo"]


def test_unsupported_currency_rejected():
    clean, errors = _validate(_row(moneda="XXX"))
    assert clean.empty
    assert errors.iloc[0]["campo"] == "moneda"


def test_invalid_type_rejected():
    clean, errors = _validate(_row(tipo="OTRO"))
    assert clean.empty
    assert errors.iloc[0]["campo"] == "tipo"


def test_due_before_issue_rejected():
    clean, errors = _validate(
        _row(fecha_emision="2026-03-01", fecha_vencimiento="2026-01-01")
    )
    assert clean.empty
    assert errors.iloc[0]["campo"] == "fecha_vencimiento"


def test_missing_required_field_rejected():
    clean, errors = _validate(_row(cliente_proveedor=""))
    assert clean.empty
    assert errors.iloc[0]["campo"] == "cliente_proveedor"


def test_only_invalid_rows_are_dropped():
    clean, errors = _validate(_row(id=1), _row(id=2, monto=-1), _row(id=3))
    assert list(clean["id"]) == [1, 3]
    assert len(errors) == 1
