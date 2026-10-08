"""Preparação e agregações da base simulada do Tema 19."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
NUMERICAS = ["ano", "mes", "area_desmatada_km2", "area_preservada_km2", "focos_queimada", "chuva_mm", "temperatura_media", "emissoes_co2", "unidades_conservacao"]
CATEGORIAS = ["regiao", "uf", "bioma", "nivel_risco"]

def carregar():
    original = pd.read_csv(BASE / "dados/simulacao_desmatamento_brasil.csv", encoding="utf-8-sig")
    df = original.copy()
    for c in CATEGORIAS:
        df[c] = df[c].astype("string").str.strip()
    for c in NUMERICAS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    duplicadas = int(df.duplicated().sum())
    df = df.drop_duplicates()
    validas = df[NUMERICAS + CATEGORIAS + ["data"]].notna().all(axis=1)
    validas &= df["ano"].between(2015, 2024) & df["mes"].between(1, 12)
    validas &= df["data"].dt.year.eq(df["ano"]) & df["data"].dt.month.eq(df["mes"])
    validas &= df[[c for c in NUMERICAS if c != "temperatura_media"]].ge(0).all(axis=1)
    validas &= df["nivel_risco"].isin(["Baixo", "Médio", "Alto", "Crítico"])
    removidas = int((~validas).sum())
    df = df.loc[validas].copy()
    for c in ["ano", "mes", "focos_queimada", "unidades_conservacao"]:
        if not df[c].mod(1).eq(0).all():
            raise ValueError(f"Valores fracionários inesperados em {c}")
        df[c] = df[c].astype(int)
    df["trimestre"] = df["data"].dt.quarter
    df["periodo"] = df["data"].dt.to_period("M").astype(str)
    df["risco_elevado"] = df["nivel_risco"].isin(["Alto", "Crítico"])
    return df.sort_values("data").reset_index(drop=True), {
        "linhas_originais": len(original), "duplicadas_removidas": duplicadas,
        "invalidas_removidas": removidas, "linhas_validas": len(df),
        "ausentes_originais": int(original.isna().sum().sum())}

def ranking(df, coluna):
    return df.groupby(coluna, observed=True)["area_desmatada_km2"].sum().sort_values(ascending=False)

def indicadores(df):
    return {"desmatamento": df.area_desmatada_km2.sum(),
            "preservacao": df.area_preservada_km2.sum(),
            "queimadas": int(df.focos_queimada.sum()),
            "co2": df.emissoes_co2.sum(),
            "bioma": ranking(df, "bioma").index[0] if len(df) else "—",
            "estado": ranking(df, "uf").index[0] if len(df) else "—"}

def numero(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
