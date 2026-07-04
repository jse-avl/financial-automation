# Automatización de Conciliación y Reporte Financiero

Pipeline en Python para conciliación de cuentas por cobrar (CxC) y cuentas por pagar (CxP) con conversión automática a USD usando tasas de cambio actualizadas vía API.

## Problema que resuelve

Empresas del sector construcción y maquinaria pesada manejan compras e importaciones en múltiples monedas (USD, EUR, MXN, CNY, etc.). Este proyecto automatiza:

- Lectura de facturas desde un archivo CSV
- Consulta de tasas de cambio actualizadas (API Frankfurter, sin API key)
- Validación de datos (montos negativos, fechas inválidas, monedas no soportadas)
- Conversión de todos los montos a USD
- Cálculo de métricas clave: total CxC, total CxP, flujo de caja neto
- Clasificación de antigüedad de facturas vencidas (aging)
- Generación de reporte Excel profesional con formato condicional
- Dashboard interactivo en Streamlit

## Stack tecnológico

- Python 3.11+
- pandas (manipulación de datos)
- requests (consumo de API)
- openpyxl (generación de Excel)
- streamlit (dashboard interactivo)

## Estructura del proyecto

```
financial-automation/
├── data/
│   └── cuentas_sample.csv        # Dataset simulado (45 facturas)
├── src/
│   ├── fetch_rates.py            # Consulta API Frankfurter con cache
│   ├── validate.py               # Validación de datos
│   ├── transform.py              # Conversión a USD y métricas
│   ├── report.py                 # Generación de Excel con formato
│   └── main.py                   # Orquestador del pipeline
├── dashboard/
│   └── app.py                    # Dashboard Streamlit
├── output/
│   └── reporte_financiero.xlsx   # Reporte generado
├── requirements.txt
└── README.md
```

## Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el pipeline

```bash
python src/main.py
```

Esto genera el archivo `output/reporte_financiero.xlsx` con tres hojas:
- **Resumen Ejecutivo**: métricas principales, top 5 vencidas, tasas usadas
- **Detalle**: todas las facturas validadas con monto USD y clasificación aging
- **Inconsistencias**: filas descartadas con el motivo del error

### 3. Dashboard interactivo (opcional)

```bash
streamlit run dashboard/app.py
```

## Dataset de prueba

El archivo `data/cuentas_sample.csv` contiene 45 facturas simuladas con:
- Monedas: USD, EUR, MXN, CNY (importaciones realistas de maquinaria)
- Clientes y proveedores del sector construcción peruano
- Facturas en múltiples estados de vencimiento
- Errores inyectados intencionalmente: montos negativos, monedas no soportadas, fechas inversas, campos vacíos

## Notas

- Las tasas de cambio se consultan a la API pública de [Frankfurter](https://api.frankfurter.dev) y se cachean localmente para evitar llamadas repetidas el mismo día
- El proyecto simula un caso de uso real de automatización financiera con validación previa a distribución gerencial
- Desarrollado como proyecto de portafolio para el perfil "Analista Programador de Automatización Financiera"
