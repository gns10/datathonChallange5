import streamlit as st
from mlBackEnd import featuringEngineering,  createModel, recebeDados, defasagem_aluno

st.set_page_config(page_title="ML do aluno")

st.title("Probabilidade de Defasagem")

defasagem = st.number_input("Defasagem", value=0.0)
ian = st.number_input("IAN", value=7.0)
ida = st.number_input("IDA", value=7.0)
nota_mat = st.number_input("Nota Matemática", value=7.0)
nota_port = st.number_input("Nota Português", value=7.0)
nota_ing = st.number_input("Nota Inglês", value=0.0)
ieg = st.number_input("IEG", value=7.0)
ips = st.number_input("IPS", value=7.0)
ipp = st.number_input("IPP", value=7.0)
idade = st.number_input("Idade", value=12)
ano_ingresso = st.number_input("Ano de Ingresso", value=2020)

# Botão
if st.button("Calcular Risco"):
    df_modelo = featuringEngineering()
    model = createModel(df_modelo)  
    # Base com inputs
    dados = recebeDados(
        defasagem = defasagem,
        ian = ian,
        ida = ida,
        nota_mat = nota_mat,
        nota_port = nota_port,
        nota_ing = nota_ing,
        ieg = ieg,
        ips = ips,
        ipp = ipp,
        idade = idade,
        ano_ingresso = ano_ingresso
    )

    prob_risco = defasagem_aluno(dados)
    # Saída
    st.subheader("Resultado")
    st.metric(
        label="Probabilidade de risco de defasagem",
        value=f"{prob_risco:.2%}"
    )