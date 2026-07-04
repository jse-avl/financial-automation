import os
import sys
from datetime import date

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetch_rates import get_exchange_rates
from src.transform import calcular_aging, calcular_metricas, convertir_moneda
from src.validate import validate_dataframe

st.set_page_config(
    page_title="Automatización Financiera",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Dashboard de Automatización Financiera")
st.markdown(
    "Pipeline de conciliación y reporte financiero con tipo de cambio — "
    "construcción y maquinaria pesada"
)

ruta_csv = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "cuentas_sample.csv",
)

try:
    df = pd.read_csv(ruta_csv, parse_dates=["fecha_emision", "fecha_vencimiento"])
except FileNotFoundError:
    st.error(f"No se encuentra el archivo CSV en {ruta_csv}")
    st.stop()

with st.spinner("Obteniendo tasas de cambio..."):
    try:
        rates = get_exchange_rates("USD")
    except ConnectionError as e:
        st.error(f"Error obteniendo tasas: {e}")
        st.stop()

df_clean, df_errors = validate_dataframe(df, rates)
df_clean = convertir_moneda(df_clean, rates)
df_clean = calcular_aging(df_clean)
metrics = calcular_metricas(df_clean)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total CxC (USD)", f"${metrics['total_cxc_usd']:,.2f}")
col2.metric("Total CxP (USD)", f"${metrics['total_cxp_usd']:,.2f}")
col3.metric(
    "Flujo Neto (USD)",
    f"${metrics['flujo_neto_usd']:,.2f}",
    delta="Positivo" if metrics["flujo_neto_usd"] > 0 else "Negativo",
)
col4.metric("Errores en datos", len(df_errors))

st.subheader("Detalle de Facturas")
vencidas = df_clean["dias_vencido"] > 0
mostrar_solo_vencidas = st.checkbox("Mostrar solo facturas vencidas")
df_display = df_clean[vencidas] if mostrar_solo_vencidas else df_clean

cols_mostrar = [
    "id", "tipo", "cliente_proveedor", "moneda", "monto",
    "monto_usd", "dias_vencido", "aging",
]
st.dataframe(
    df_display[cols_mostrar].style.format(
        {"monto": "${:,.2f}", "monto_usd": "${:,.2f}"}
    ),
    use_container_width=True,
    height=400,
)

st.subheader("Distribución por Aging")
aging_counts = df_clean["aging"].value_counts().reindex(
    ["Al día", "0-30 días", "31-60 días", "61-90 días", "+90 días"],
    fill_value=0,
)
st.bar_chart(aging_counts)

if not df_errors.empty:
    st.subheader("Inconsistencias Encontradas")
    st.dataframe(df_errors, use_container_width=True)

st.subheader("Tasas de Cambio Aplicadas")
df_rates = pd.DataFrame(
    [{"Moneda": k, "Tasa (1 USD)": round(v, 4)} for k, v in rates.items()]
)
st.dataframe(df_rates, use_container_width=True)

st.caption(f"Reporte generado el {date.today().strftime('%d/%m/%Y')}")
