from datetime import date

import pandas as pd


def convertir_moneda(df, rates):
    df = df.copy()
    df["monto_usd"] = df.apply(
        lambda r: float(r["monto"]) / rates[str(r["moneda"]).strip()], axis=1
    )
    df["monto_usd"] = df["monto_usd"].round(2)
    return df


def calcular_aging(df):
    df = df.copy()
    hoy = date.today()
    df["dias_vencido"] = df["fecha_vencimiento"].apply(
        lambda fv: (hoy - fv.date()).days
        if pd.notna(fv)
        else 0
    )

    def clasificar(dias):
        if dias <= 0:
            return "Al día"
        if dias <= 30:
            return "0-30 días"
        if dias <= 60:
            return "31-60 días"
        if dias <= 90:
            return "61-90 días"
        return "+90 días"

    df["aging"] = df["dias_vencido"].apply(clasificar)
    return df


def calcular_metricas(df):
    total_cxc = df[df["tipo"] == "CxC"]["monto_usd"].sum()
    total_cxp = df[df["tipo"] == "CxP"]["monto_usd"].sum()

    return {
        "total_cxc_usd": round(total_cxc, 2),
        "total_cxp_usd": round(total_cxp, 2),
        "flujo_neto_usd": round(total_cxc - total_cxp, 2),
    }
