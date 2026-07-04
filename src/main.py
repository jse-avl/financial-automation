import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetch_rates import get_exchange_rates
from src.report import generar_reporte
from src.transform import calcular_aging, calcular_metricas, convertir_moneda
from src.validate import validate_dataframe


def main():
    ruta_csv = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "cuentas_sample.csv",
    )

    if not os.path.exists(ruta_csv):
        print(f"ERROR: No se encuentra el archivo {ruta_csv}")
        sys.exit(1)

    try:
        df = pd.read_csv(
            ruta_csv, parse_dates=["fecha_emision", "fecha_vencimiento"]
        )
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        sys.exit(1)

    try:
        rates = get_exchange_rates("USD")
        print(f"Tasas obtenidas: {len(rates)} monedas disponibles")
    except ConnectionError as e:
        print(f"ERROR obteniendo tasas: {e}")
        sys.exit(1)

    df_clean, df_errors = validate_dataframe(df, rates)
    print(f"Filas válidas: {len(df_clean)} | Errores: {len(df_errors)}")

    df_clean = convertir_moneda(df_clean, rates)
    df_clean = calcular_aging(df_clean)
    metrics = calcular_metricas(df_clean)

    ruta_output = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "reporte_financiero.xlsx",
    )
    os.makedirs(os.path.dirname(ruta_output), exist_ok=True)

    generar_reporte(df_clean, df_errors, metrics, rates, ruta_output)

    print(f"\n{'='*50}")
    print(f"Total CxC (USD):      ${metrics['total_cxc_usd']:>12,.2f}")
    print(f"Total CxP (USD):      ${metrics['total_cxp_usd']:>12,.2f}")
    print(f"Flujo de caja neto:   ${metrics['flujo_neto_usd']:>12,.2f}")
    print(f"{'='*50}")
    print(f"Facturas vencidas:     {len(df_clean[df_clean['dias_vencido'] > 0])}")
    print(f"Inconsistencias:       {len(df_errors)}")
    print(f"Reporte generado:     {ruta_output}")


if __name__ == "__main__":
    main()
