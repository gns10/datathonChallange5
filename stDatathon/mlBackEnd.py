import pandas as pd
import joblib
from modelo import padronizar_base
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

excel_path = os.path.join(
    BASE_DIR,
    "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
)

df_2024 = pd.read_excel(excel_path, sheet_name='PEDE2024')
df_2023 = pd.read_excel(excel_path, sheet_name='PEDE2023')
df_2022 = pd.read_excel(excel_path, sheet_name='PEDE2022')
# # Featuring engineering
# ## Arredondamento dos dados numéricos
def featuringEngineering():
    # Definindo colunas padrão
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


    # Corrigindo as variáveis abaixo para numérico
    for col in ['FASE', 'IDADE']:
        df_modelo[col] = pd.to_numeric(df_modelo[col], errors='coerce')

    return df_modelo


def createModel(df_modelo):
    # Ordenação da base
    df = df_modelo.copy()
    df = df.sort_values(['RA', 'ANO'])

    #Criação da variação da defasagem
    df['DELTA_DEFASAGEM'] = (
        df
        .groupby('RA')['DEFASAGEM']
        .diff()
    )

    df['TARGET_RISCO'] = (df['DELTA_DEFASAGEM'] >= 0).astype(int)

    #Mantendo apenas alunos com histórico válido Delta diferented zero
    df_model = df[df['DELTA_DEFASAGEM'].notna()].copy()

    FEATURES = [
    # Estado atual
    'DEFASAGEM',
    'IAN',
    
    # Acadêmico
    'IDA',
    'NOTA_MAT',
    'NOTA_PORT',
    'NOTA_ING',
    
    # Engajamento e suporte
    'IEG',
    'IPS',
    'IPP',
    
    # Controle
    'IDADE',
    'ANO_INGRESSO'
    ]

    X = df_model[FEATURES]
    y = df_model['TARGET_RISCO']

    for col in FEATURES:
        X[f'{col}_MISS'] = X[col].isna().astype(int)

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # Separação do treino x teste

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)


    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )

    modelo = LogisticRegression(
        max_iter=1000,
        class_weight='balanced'
    )

    modelo.fit(X_train, y_train)
    joblib.dump(modelo, 'modelo.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(imputer, 'imputer.pkl')
    return modelo


# Função interativa para input de dados
def recebeDados(defasagem, ian, ida, nota_mat, nota_port, nota_ing, ieg, ips, ipp, idade, ano_ingresso):
    # Base com inputs
    dados = pd.DataFrame([{
        'DEFASAGEM': defasagem,
        'IAN': ian,
        'IDA': ida,
        'NOTA_MAT': nota_mat,
        'NOTA_PORT': nota_port,
        'NOTA_ING': nota_ing,
        'IEG': ieg,
        'IPS': ips,
        'IPP': ipp,
        'IDADE': idade,
        'ANO_INGRESSO': ano_ingresso
    }])

    
    return dados

def defasagem_aluno(dados):
    modelo = joblib.load("modelo.pkl")
    scaler = joblib.load("scaler.pkl")
    imputer = joblib.load("imputer.pkl")
    for col in dados.columns:
        dados[f'{col}_MISS'] = dados[col].isna().astype(int)

    # Imputação + escala
    X_imp = imputer.transform(dados)
    X_scaled = scaler.transform(X_imp)

    # Predição
    prob_risco = modelo.predict_proba(X_scaled)[0, 1]

    return prob_risco



