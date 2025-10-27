import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meu Agente IA", page_icon="🤖")

st.title("🤖 Meu Agente de Sistemas")
st.write("Faça upload de um Excel ou descreva seu sistema!")

# Upload de arquivo
uploaded_file = st.file_uploader("📤 Upload Excel", type=['xlsx'])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📊 Dados do arquivo:")
    st.dataframe(df)

# Conversa
user_input = st.text_area("💬 Descreva seu sistema:")
if st.button("🚀 Gerar Escopo"):
    st.success("Escopo gerado com sucesso!")
    st.write("Aqui viria o escopo técnico...")
