import streamlit as st
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos 5 anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)
ano = st.radio('Escolha um ano para análise:',
                                    ('2020', '2021', '2022', '2023', '2024'))

filtro = st.selectbox('Escolha uma variável para análise:',
                                    sorted(['Renda', 'Ano de conclusão', 'Raça']))
