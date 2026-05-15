import streamlit as st
from mlBackEnd import recebeDados, defasagem_aluno
import joblib

#df_modelo = baseNormalizada()
#createModel(df_modelo)  

st.set_page_config(page_title="ML do aluno")


artefato = joblib.load("modelo_risco_defasagem.pkl")
st.title("Probabilidade de Defasagem")

genero = st.radio("Gênero", ('Masculino', 'Feminino'), index=0)
if genero == 'Masculino':
    genero = 1
else:
    genero = 0
ian = st.number_input("IAN", value=7.0)
ida = st.number_input("IDA", value=7.0)
tempo_associacao = st.number_input("Tempo na Associação", value=1)
ensino_grupo = st.radio("Ensino Grupo", ('Privado', 'Público'), index=0)
if ensino_grupo == 'Privado':
    ensino_privado = 1
    ensino_publico = 0
else:
    ensino_publico = 1
    ensino_privado = 0
ieg = st.number_input("IEG", value=7.0)
ips = st.number_input("IPS", value=7.0)
ipp = st.number_input("IPP", value=7.0)
idade = st.number_input("Idade", value=12)

# Botão
if st.button("Calcular Risco"):    
    # Base com inputs
    dados = recebeDados(
        IDA= ida,
        IEG= ieg,
        IPS= ips,
        IPP= ipp,
        IAN= ian,
        IDADE= idade,
        GENERO= genero,
        TEMPO_ASSOCIACAO= tempo_associacao,
        ENSINO_GRUPO_Privada= ensino_privado,
        ENSINO_GRUPO_Pública= ensino_publico,
    )
    prob_risco = defasagem_aluno(dados, artefato)
    # Saída
    st.subheader("Resultado")
    st.metric(
        label="Probabilidade de risco de defasagem",
        value=f"{prob_risco:.2%}"
    )