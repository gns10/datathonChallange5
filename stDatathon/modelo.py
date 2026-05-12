# backend/modelo.py
import pandas as pd

def padronizar_base(df, map_colunas, ano, colunas_padrao):
    df = df.copy()

    # Renomear colunas
    df = df.rename(columns=map_colunas)

    # Adicionar coluna de ano
    df['ANO'] = ano

    # Criar colunas que não existirem
    for col in colunas_padrao:
        if col not in df.columns:
            df[col] = pd.NA

    # Selecionar apenas o schema final
    df = df[list(colunas_padrao)]

    return df