from datetime import datetime
import pandas as pd
import joblib
import numpy as np
from modelo import  corrigir_idade
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def createModel(df_modelo):

    df_modelo = df_modelo.sort_values(
    ["RA", "ANO"]
)

    df_modelo["DELTA_DEFASAGEM"] = (
        df_modelo.groupby("RA")["DEFASAGEM"]
        .diff()
    )
    df = df_modelo
    df["TARGET_RISCO"] = np.where(

    # piorou
    df["DELTA_DEFASAGEM"] > 0,

    1,

    np.where(

        # já estava defasado e continua
        (
            (df["DELTA_DEFASAGEM"] == 0)
            &
            (df["IAN"] < 10)
        ),

        1,

        0
    )
)
    df_model = df[df['DELTA_DEFASAGEM'].notna()].copy()
    
    FEATURES = [

    # Acadêmico
    'IDA',

    # Engajamento / suporte
    'IEG',
    'IPS',
    'IPP',

    # Estado atual do aluno
    'IAN',

    # Perfil
    'IDADE',
    'GENERO',
    'ENSINO_GRUPO',

    # Tempo na associação
    'TEMPO_ASSOCIACAO'
    ]

    X = df_model[FEATURES]
    y = df_model['TARGET_RISCO']

    df_model["IDADE"] = (
        df_model["IDADE"]
        .apply(corrigir_idade)
        )

    X["GENERO"] = (
        X["GENERO"]
        .map({
            "Feminino": 0,
            "Masculino": 1
        })
    )

    X = pd.get_dummies(
        X,
        columns=["ENSINO_GRUPO"],
        drop_first=True
    )

    X = X.copy()

    imputer = SimpleImputer(
        strategy="median"
    )
    
    X['IDADE'] = pd.to_numeric(X['IDADE'], errors='coerce')

    X_imputed = pd.DataFrame(
        imputer.fit_transform(X),
        columns=X.columns,
        index=X.index
    )

    # ====================================
    # Padronização (escala)
    # ====================================
    scaler = StandardScaler()

    X_scaled = pd.DataFrame(
        scaler.fit_transform(X_imputed),
        columns=X.columns,
        index=X.index
    )

    X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
    )

    model = LogisticRegression(
        class_weight='balanced',
        random_state=42,
        max_iter=1000
    )

    # treino
    model.fit(X_train, y_train)

    artefato_modelo = {

        "model": model,  # ou calibrated_model se quiser usar calibrado

        "scaler": scaler,

        "imputer": imputer,

        "features": X.columns.tolist(),

        # opcional para o streamlit
        "threshold": 0.50
    }

    joblib.dump(
        artefato_modelo,
        "modelo_risco_defasagem.pkl")


# Função interativa para input de dados
def recebeDados(IAN, IDA, GENERO, TEMPO_ASSOCIACAO, ENSINO_GRUPO_Privada, ENSINO_GRUPO_Pública, IEG, IPS, IPP, IDADE):
    # Base com inputs
    dados = pd.DataFrame([{
        "IDA": IDA,
        "IEG": IEG,
        "IPS": IPS,
        "IPP": IPP,
        "IAN": IAN,
        "IDADE": IDADE,
        "GENERO": GENERO,
        "TEMPO_ASSOCIACAO": TEMPO_ASSOCIACAO,
        "ENSINO_GRUPO_Privada": ENSINO_GRUPO_Privada,
        "ENSINO_GRUPO_Pública": ENSINO_GRUPO_Pública,
    }])

    
    return dados

def defasagem_aluno(dados, artefato):

    model = artefato["model"]
    scaler = artefato["scaler"]
    imputer = artefato["imputer"]
    features = artefato["features"]

    # garantir mesmas colunas do treino
    dados = dados[features].copy()

    # imputar
    dados_imp = pd.DataFrame(
        imputer.transform(dados),
        columns=features
    )

    # escalar
    dados_scaled = pd.DataFrame(
        scaler.transform(dados_imp),
        columns=features
    )

    # previsão
    dados["PROB_RISCO"] = model.predict_proba(dados_scaled)[:, 1]

    return dados["PROB_RISCO"].iloc[0]



