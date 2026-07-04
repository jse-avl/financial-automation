import pandas as pd


COLUMNAS_OBLIGATORIAS = ["id", "tipo", "cliente_proveedor", "moneda", "monto"]


def validate_dataframe(df, rates):
    errores = []
    indices_invalidos = set()

    monedas_soportadas = set(rates.keys())

    for idx, row in df.iterrows():
        for col in COLUMNAS_OBLIGATORIAS:
            if pd.isna(row.get(col)) or str(row.get(col, "")).strip() == "":
                errores.append({
                    "fila": idx,
                    "campo": col,
                    "motivo": "Campo obligatorio vacío",
                })
                indices_invalidos.add(idx)

        if pd.notna(row.get("tipo")):
            if str(row["tipo"]).strip() not in ("CxC", "CxP"):
                errores.append({
                    "fila": idx,
                    "campo": "tipo",
                    "motivo": "Tipo debe ser CxC o CxP",
                })
                indices_invalidos.add(idx)

        if pd.notna(row.get("moneda")):
            moneda = str(row["moneda"]).strip()
            if moneda not in monedas_soportadas:
                errores.append({
                    "fila": idx,
                    "campo": "moneda",
                    "motivo": f"Moneda '{moneda}' no soportada",
                })
                indices_invalidos.add(idx)

        if pd.notna(row.get("monto")):
            try:
                monto = float(row["monto"])
                if monto <= 0:
                    errores.append({
                        "fila": idx,
                        "campo": "monto",
                        "motivo": "Monto debe ser positivo",
                    })
                    indices_invalidos.add(idx)
            except (ValueError, TypeError):
                errores.append({
                    "fila": idx,
                    "campo": "monto",
                    "motivo": "Monto no es un número válido",
                })
                indices_invalidos.add(idx)

        if pd.notna(row.get("fecha_vencimiento")) and pd.notna(
            row.get("fecha_emision")
        ):
            try:
                fv = pd.to_datetime(row["fecha_vencimiento"])
                fe = pd.to_datetime(row["fecha_emision"])
                if fv < fe:
                    errores.append({
                        "fila": idx,
                        "campo": "fecha_vencimiento",
                        "motivo": "Fecha de vencimiento anterior a fecha de emisión",
                    })
                    indices_invalidos.add(idx)
            except Exception:
                errores.append({
                    "fila": idx,
                    "campo": "fecha_vencimiento",
                    "motivo": "Fecha inválida",
                })
                indices_invalidos.add(idx)

    df_limpio = df.drop(index=indices_invalidos).copy()
    df_errores = pd.DataFrame(errores, columns=["fila", "campo", "motivo"])

    return df_limpio, df_errores
