from modelo import padronizar_base, padronizar_fase, padronizar_fase_ideal, map_ensino_grupo
import pandas as pd
import os

def normalizandoBase():
# Definindo colunas padrão
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    excel_path = os.path.join(
        BASE_DIR,
        "baseDados.xlsx")

    df_2024 = pd.read_excel(excel_path, sheet_name='PEDE2024')
    df_2023 = pd.read_excel(excel_path, sheet_name='PEDE2023')
    df_2022 = pd.read_excel(excel_path, sheet_name='PEDE2022')


    COLUNAS_PADRAO = {
    # Identificação
    'RA',
    'NOME',
    'ANO',
    'FASE',
    'FASE_IDEAL',
    'DEFASAGEM',
    'IAN',
    'IDA',
    'NOTA_MAT',
    'NOTA_PORT',
    'NOTA_ING',
    'IEG',
    'IPS',
    'IPP',
    'ANO_INGRESSO',
    'INSTITUICAO_ENSINO',
    'GENERO',
    'IDADE'
}

    MAP_2022 = {
    'RA': 'RA',
    'Nome': 'NOME',
    'Fase': 'FASE',
    'Fase ideal': 'FASE_IDEAL',
    'Defas': 'DEFASAGEM',
    'IAN': 'IAN',
    'IDA': 'IDA',
    'Matem': 'NOTA_MAT',
    'Portug': 'NOTA_PORT',
    'Inglês': 'NOTA_ING',
    'IEG': 'IEG',
    'IPS': 'IPS',
    'IAA': 'IAA', 
    'Ano ingresso': 'ANO_INGRESSO',
    'Instituição de ensino': 'INSTITUICAO_ENSINO',
    'Gênero': 'GENERO',
    'Idade 22': 'IDADE'
}

    MAP_2023 = {
    'RA': 'RA',
    'Nome Anonimizado': 'NOME',
    'Fase': 'FASE',
    'Fase Ideal': 'FASE_IDEAL',
    'Defasagem': 'DEFASAGEM',
    'IAN': 'IAN',
    'IDA': 'IDA',
    'Mat': 'NOTA_MAT',
    'Por': 'NOTA_PORT',
    'Ing': 'NOTA_ING',
    'IEG': 'IEG',
    'IPS': 'IPS',
    'IPP': 'IPP',
    'Ano ingresso': 'ANO_INGRESSO',
    'Instituição de ensino': 'INSTITUICAO_ENSINO',
    'Gênero': 'GENERO',
    'Idade': 'IDADE'
}

    MAP_2024 = {
    'RA': 'RA',
    'Nome Anonimizado': 'NOME',
    'Fase': 'FASE',
    'Fase Ideal': 'FASE_IDEAL',
    'Defasagem': 'DEFASAGEM',
    'IAN': 'IAN',
    'IDA': 'IDA',
    'Mat': 'NOTA_MAT',
    'Por': 'NOTA_PORT',
    'Ing': 'NOTA_ING',
    'IEG': 'IEG',
    'IPS': 'IPS',
    'IPP': 'IPP',
    'Ano ingresso': 'ANO_INGRESSO',
    'Instituição de ensino': 'INSTITUICAO_ENSINO',
    'Gênero': 'GENERO',
    'Idade': 'IDADE'
}


    df_2022_std = padronizar_base(df_2022, MAP_2022, 2022, COLUNAS_PADRAO)
    df_2023_std = padronizar_base(df_2023, MAP_2023, 2023, COLUNAS_PADRAO)
    df_2024_std = padronizar_base(df_2024, MAP_2024, 2024, COLUNAS_PADRAO)

    #Trazendo todos os dados para um df único modelo
    df_modelo = pd.concat([df_2022_std, df_2023_std, df_2024_std])

    return df_modelo

def baseNormalizada():
    df_modelo = normalizandoBase()
    df_modelo["FASE_PADRONIZADA"] = df_modelo["FASE"].apply(padronizar_fase)

    df_modelo["FASE_IDEAL_PADRONIZADA"] = (
        df_modelo["FASE_IDEAL"]
        .apply(padronizar_fase_ideal)
    )

    # ==========================================================
    # 5) Criar versão ordinal
    # ==========================================================
    mapa_fase_num = {
        "ALFA": 0,
        "FASE 1": 1,
        "FASE 2": 2,
        "FASE 3": 3,
        "FASE 4": 4,
        "FASE 5": 5,
        "FASE 6": 6,
        "FASE 7": 7,
        "FASE 8": 8
    }

    df_modelo["FASE_NUM"] = (
        df_modelo["FASE_PADRONIZADA"]
        .map(mapa_fase_num)
    )

    df_modelo["FASE_IDEAL_NUM"] = (
        df_modelo["FASE_IDEAL_PADRONIZADA"]
        .map(mapa_fase_num)
    )

    df_modelo["TEMPO_ASSOCIACAO"] = (
        df_modelo["ANO"] - df_modelo["ANO_INGRESSO"]
    )

    # Garantir numérico
    colunas_num = [
        "IAN", "IDA", "IEG",
        "IPS", "IPP",
        "TEMPO_ASSOCIACAO"
    ]

    for c in colunas_num:
        df_modelo[c] = pd.to_numeric(df_modelo[c], errors="coerce")

    df_modelo["ENSINO_GRUPO"] = df_modelo["INSTITUICAO_ENSINO"].apply(map_ensino_grupo)

    map_genero = {
        "Menina": "Feminino",
        "Feminino": "Feminino",

        "Menino": "Masculino",
        "Masculino": "Masculino"
    }

    df_modelo["GENERO"] = (
        df_modelo["GENERO"]
        .str.strip()
        .map(map_genero)
    )

    return df_modelo