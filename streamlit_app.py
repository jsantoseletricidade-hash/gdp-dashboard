from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="JS SANTOS ELETRICIDADE", page_icon="⚡", layout="wide")

st.title("⚡ JS SANTOS ELETRICIDADE")
st.subheader("Painel de Gestão e Controlo de Funcionários")

menu = st.sidebar.selectbox("Navegação", ["Registo Diário", "Mapa Semanal", "Férias"])

if menu == "Registo Diário":
    st.markdown("### Registo de Trabalhos")
    cliente = st.text_input("Cliente / Obra")
    funcionario = st.text_input("Nome do Funcionário")
    horas = st.number_input("Horas", min_value=0.0, value=8.0)
    
    if st.button("Guardar"):
        if cliente and funcionario:
            st.success("Registo guardado com sucesso!")
        else:
            st.warning("Preencha o cliente e o funcionário.")

elif menu == "Mapa Semanal":
    st.markdown("### Mapa Semanal")
    st.info("Consulte a distribuição semanal da equipa.")

elif menu == "Férias":
    st.markdown("### Gestão de Férias")
    st.info("Consulte o mapa de férias.")
