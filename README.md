# Automatización de Conciliación y Reporte Financiero
# Financial Reconciliation and Reporting Automation

---

## Español

Pipeline en Python para conciliación de cuentas por cobrar (CxC) y cuentas por pagar (CxP) con conversión automática a USD usando tasas de cambio actualizadas vía API.

**Problema que resuelve:** Empresas del sector construcción y maquinaria pesada manejan compras e importaciones en múltiples monedas (USD, EUR, MXN, CNY, etc.). Este proyecto automatiza:

- Lectura de facturas desde un archivo CSV
- Consulta de tasas de cambio actualizadas (API Frankfurter, sin API key)
- Validación de datos (montos negativos, fechas inválidas, monedas no soportadas)
- Conversión de todos los montos a USD
- Cálculo de métricas clave: total CxC, total CxP, flujo de caja neto
- Clasificación de antigüedad de facturas vencidas (aging)
- Generación de reporte Excel profesional con formato condicional
- Dashboard interactivo en Streamlit

### Stack tecnológico

- Python 3.11+
- pandas, requests, openpyxl, streamlit

### Estructura del proyecto

```
financial-automation/
├── data/cuentas_sample.csv         # Dataset simulado (45 facturas)
├── src/fetch_rates.py              # Consulta API Frankfurter con cache
├── src/validate.py                 # Validación de datos
├── src/transform.py                # Conversión a USD y métricas
├── src/report.py                   # Generación de Excel con formato
├── src/main.py                     # Orquestador del pipeline
├── dashboard/app.py                # Dashboard Streamlit
├── output/reporte_financiero.xlsx  # Reporte generado
├── requirements.txt
└── README.md
```

### Cómo ejecutar

```bash
pip install -r requirements.txt
python src/main.py
streamlit run dashboard/app.py   # Dashboard opcional
```

### Dataset de prueba

45 facturas simuladas con monedas USD, EUR, MXN, CNY. Incluye errores inyectados intencionalmente para probar la validación.

---

## English

Python pipeline for accounts receivable (AR) and accounts payable (AP) reconciliation with automatic USD conversion using up-to-date exchange rates via API.

**Problem it solves:** Construction and heavy machinery companies handle purchases and imports in multiple currencies (USD, EUR, MXN, CNY, etc.). This project automates:

- Reading invoices from a CSV file
- Fetching live exchange rates (Frankfurter API, no API key required)
- Data validation (negative amounts, invalid dates, unsupported currencies)
- Converting all amounts to USD
- Calculating key metrics: total AR, total AP, net cash flow
- Aging classification for overdue invoices
- Generating professional Excel reports with conditional formatting
- Interactive Streamlit dashboard

### Tech Stack

- Python 3.11+
- pandas, requests, openpyxl, streamlit

### Project Structure

```
financial-automation/
├── data/cuentas_sample.csv         # Simulated dataset (45 invoices)
├── src/fetch_rates.py              # Frankfurter API client with cache
├── src/validate.py                 # Data validation rules
├── src/transform.py                # USD conversion & metrics
├── src/report.py                   # Excel report generation
├── src/main.py                     # Pipeline orchestrator
├── dashboard/app.py                # Streamlit dashboard
├── output/reporte_financiero.xlsx  # Generated report
├── requirements.txt
└── README.md
```

### How to Run

```bash
pip install -r requirements.txt
python src/main.py
streamlit run dashboard/app.py   # Optional dashboard
```

### Test Dataset

45 simulated invoices in USD, EUR, MXN, CNY. Includes intentionally injected errors to test validation logic.
