# backend/modelo.py
import pandas as pd
import unicodedata
import numpy as np
import re
from datetime import datetime

def padronizar_base(df, map_colunas, ano, COLUNAS_PADRAO):
    df = df.copy()

    # Renomear colunas
    df = df.rename(columns=map_colunas)

    # Adicionar coluna de ano
    df['ANO'] = ano

    # Criar colunas que não existirem
    for col in COLUNAS_PADRAO:
        if col not in df.columns:
            df[col] = pd.NA

    # Selecionar apenas o schema final
    df = df[list(COLUNAS_PADRAO)]

    return df

def strip_accents(s):
    if pd.isna(s):
        return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))




def normalize_text(x):
    s = strip_accents(x)
    s = s.upper().strip()
    s = " ".join(s.split())
    return s


# ==========================================================
# 2) Padronizar FASE
# ==========================================================
def padronizar_fase(v):

    if pd.isna(v):
        return np.nan

    s = normalize_text(v)

    # -----------------------------------------
    # Casos numéricos puros
    # -----------------------------------------
    try:
        num = int(float(s))

        mapa_num = {
            0: "ALFA",
            1: "FASE 1",
            2: "FASE 2",
            3: "FASE 3",
            4: "FASE 4",
            5: "FASE 5",
            6: "FASE 6",
            7: "FASE 7",
            8: "FASE 8",
            9: "FASE 4"   # 9º ano
        }

        if num in mapa_num:
            return mapa_num[num]

    except:
        pass

    # -----------------------------------------
    # Já vem como FASE X
    # -----------------------------------------
    if "FASE" in s:
        match = re.search(r"FASE\s*(\d)", s)

        if match:
            fase_num = int(match.group(1))
            return f"FASE {fase_num}"

    # -----------------------------------------
    # ALFA
    # -----------------------------------------
    if "ALFA" in s:
        return "ALFA"

    # -----------------------------------------
    # Turmas (1A, 2B, 5C...)
    # -----------------------------------------
    match_turma = re.match(r"^(\d+)", s)

    if match_turma:

        serie = int(match_turma.group(1))

        # 1º e 2º ano
        if serie in [1, 2]:
            return "ALFA"

        # 3º e 4º ano
        elif serie in [3, 4]:
            return "FASE 1"

        # 5º e 6º ano
        elif serie in [5, 6]:
            return "FASE 2"

        # 7º e 8º ano
        elif serie in [7, 8]:
            return "FASE 3"

        # 9º ano
        elif serie == 9:
            return "FASE 4"

    return np.nan


# ==========================================================
# 3) Padronizar FASE_IDEAL
# ==========================================================
def padronizar_fase_ideal(v):

    if pd.isna(v):
        return np.nan

    s = normalize_text(v)

    if "ALFA" in s:
        return "ALFA"

    match = re.search(r"FASE\s*(\d)", s)

    if match:
        fase_num = int(match.group(1))
        return f"FASE {fase_num}"

    return np.nan

def corrigir_idade(x):

    if pd.isna(x):
        return np.nan

    # Se virou datetime do Excel
    if isinstance(x, (pd.Timestamp, datetime)):
        return x.day

    # Se já é número
    try:
        return int(float(x))
    except:
        return np.nan

def _strip_accents(s: str) -> str:
    """Remove acentos e normaliza string para facilitar regras."""
    if s is None:
        return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    return "".join([c for c in s if not unicodedata.combining(c)])

def norm_txt(x) -> str:
    """Normaliza: lower, sem acento, sem espaços extras."""
    if pd.isna(x):
        return ""
    s = _strip_accents(x)
    s = s.strip().lower()
    s = " ".join(s.split())
    return s

def map_ensino_grupo(v):
    s = norm_txt(v)

    if s == "":
        return "Não informado"

    # Pública
    if "publica" in s or "escola publica" in s:
        return "Pública"

    # Privada (inclui apadrinhamento, bolsa, parcerias etc.)
    if "privada" in s:
        return "Privada"

    # Redes / escolas específicas (mantidas separadas por segurança)
    if "rede decisao" in s or "escola jp ii" in s or "jp ii" in s:
        return "Rede/Específica"

    # Casos não aplicáveis / outros
    if "concluiu" in s or "nenhuma" in s or "universitario" in s or "formado" in s:
        return "Outros/Não aplicável"

    # fallback
    return "Outros/Não aplicável"