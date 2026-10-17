from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURAÇÃO GERAL, EMPRESA E LOGÓTIPO
# ==========================================
NOME_EMPRESA = "JS SANTOS ELETRICIDADE"
DIAS_FERIAS_ANUAIS = 22  # Dias úteis de férias por ano

st.set_page_config(
    page_title=f"{NOME_EMPRESA} - Gestão de Funcionários",
    page_icon="⚡",
    layout="wide",
)

# Ficheiros de dados locais (CSV)
FICHEIRO_TRABALHOS = "dados/registo_trabalhos.csv"
FICHEIRO_FERIAS = "dados/registo_ferias.csv"
FICHEIRO_MAPA = "dados/mapa_semanal.csv"
FICHEIRO_SALDO_INICIAL = "dados/saldo_inicial_ferias.csv"


# ==========================================
# FUNÇÕES DE APOIO
# ==========================================
def carregar_dados(caminho, colunas):
    if Path(caminho).exists():
        return pd.read_csv(caminho)
    return pd.DataFrame(columns=colunas)


def guardar_dados(df, caminho):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False)


# ==========================================
# INTERFACE DA APLICAÇÃO
# ==========================================
st.title(f"⚡ {NOME_EMPRESA}")
st.subheader("Painel de Gestão e Controlo de Funcionários")

# Menu lateral
menu = st.sidebar.selectbox(
    "Navegação",
    [
        "Registo Diário / Trabalhos",
        "Mapa Semanal",
        "Gestão de Férias",
        "Saldo Inicial",
    ],
)

if menu == "Registo Diário / Trabalhos":
    st.markdown("### Registo de Trabalhos e Materiais")
    
    col1, col2 = st.columns(2)
    with col1:
        data_trabalho = st.date_input("Data", date.today())
        cliente = st.text_input("Cliente / Local da Obra")
    with col2:
        horas = st.number_input("Horas Trabalhadas", min_value=0.0, value=8.0, step=0.5)
        funcionario = st.text_input("Nome do Funcionário")

    trabalhos_executados = st.text_area("Trabalhos Executados / Materiais Aplicados")

    if st.button("Guardar Registo"):
        if cliente and funcionario:
            novo_registo = pd.DataFrame(
                [{
                    "Data": data_trabalho,
                    "Funcionário": funcionario,
                    "Cliente": cliente,
                    "Horas": horas,
                    "Trabalhos": trabalhos_executados,
                }]
            )
            df_atual = carregar_dados(
                FICHEIRO_TRABALHOS, ["Data", "Funcionário", "Cliente", "Horas", "Trabalhos"]
            )
            df_atual = pd.concat([df_atual, novo_registo], ignore_index=True)
            guardar_dados(df_atual, FICHEIRO_TRABALHOS)
            st.success("Registo guardado com sucesso!")
        else:
            st.warning("Por favor, preencha pelo menos o cliente e o nome do funcionário.")

    # Mostrar registos existentes
    st.markdown("---")
    st.markdown("### Registos Anteriores")
    df_registos = carregar_dados(
        FICHEIRO_TRABALHOS, ["Data", "Funcionário", "Cliente", "Horas", "Trabalhos"]
    )
    if not df_registos.empty:
        st.dataframe(df_registos, use_container_width=True)
    else:
        st.info("Ainda não existem registos guardados.")

elif menu == "Mapa Semanal":
    st.markdown("### Mapa Semanal de Trabalhos")
    st.info("Consulte e organize a distribuição semanal da equipa.")
    df_mapa = carregar_dados(FICHEIRO_MAPA, ["Semana", "Funcionário", "Obra", "Observações"])
    if not df_mapa.empty:
        st.dataframe(df_mapa, use_container_width=True)
    else:
        st.info("Sem dados no mapa semanal.")

elif menu == "Gestão de Férias":
    st.markdown("### Marcação de Férias & Saldo")
    df_ferias = carregar_dados(FICHEIRO_FERIAS, ["Funcionário", "Data Início", "Data Fim", "Estado"])
    if not df_ferias.empty:
        st.dataframe(df_ferias, use_container_width=True)
    else:
        st.info("Ainda não existem pedidos de férias registados.")

elif menu == "Saldo Inicial":
    st.markdown("### Saldo Inicial de Férias dos Funcionários")
    df_saldo = carregar_dados(FICHEIRO_SALDO_INICIAL, ["Funcionário", "Dias Disponíveis"])
    if not df_saldo.empty:
        st.dataframe(df_saldo, use_container_width=True)
    else:
        st.info("Defina o saldo inicial de férias para cada colaborador.")