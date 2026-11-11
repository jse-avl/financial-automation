import pytest

from src import main as main_module


def test_defaults_point_to_sample_data():
    args = main_module.parse_args([])
    assert args.input == main_module.DEFAULT_INPUT
    assert args.output == main_module.DEFAULT_OUTPUT


def test_input_and_output_flags():
    args = main_module.parse_args(["--input", "a.csv", "--output", "b.xlsx"])
    assert args.input == "a.csv"
    assert args.output == "b.xlsx"


def test_missing_input_file_exits_with_error(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        main_module.main(["--input", str(tmp_path / "nope.csv")])
    assert exc.value.code == 1
    assert "No se encuentra" in capsys.readouterr().out


def test_full_run_with_custom_input(tmp_path, monkeypatch):
    csv = tmp_path / "in.csv"
    csv.write_text(
        "id,tipo,cliente_proveedor,moneda,monto,fecha_emision,fecha_vencimiento,estado\n"
        "1,CxC,ACME,USD,100,2026-01-01,2026-02-01,pendiente\n"
        "2,CxP,Prov,EUR,50,2026-01-01,2026-02-01,pendiente\n",
        encoding="utf-8",
    )
    out = tmp_path / "sub" / "reporte.xlsx"
    monkeypatch.setattr(
        main_module, "get_exchange_rates", lambda base="USD": {"USD": 1.0, "EUR": 0.5}
    )
    main_module.main(["--input", str(csv), "--output", str(out)])
    assert out.exists()
