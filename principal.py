import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_AMOSTRA.csv',
    '2021': 'ENEM_2021_FILTRADO_AMOSTRA.csv',
    '2022': 'ENEM_2022_FILTRADO_AMOSTRA.csv',
    '2023': 'ENEM_2023_FILTRADO_AMOSTRA.csv'
}
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, sep=';', encoding='latin1')    
    return df

st.title('Dashboard das notas do Enem nos últimos anos 📊')
st.header('Filtros:')

# Variáveis do Streamlit
ano = st.selectbox('Escolha o ano para a análise:', ('2020', '2021', '2022', '2023'))
filtro = st.selectbox('Escolha uma variável para análise:', sorted(['Renda', 'Ano de conclusão', 'Raça']))

if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Até 1 salário mínimo', 'Entre 1 e 3 salários mínimos', 'Entre 3 e 6 salários mínimos', 'Acima de 6 salários mínimos'])

if filtro == 'Ano de conclusão':
    ano_c = st.selectbox(
        'Escolha o período do ano de conclusão:',
        ['Entre 2007 e 2012', 'Entre 2013 e 2018', 'Entre 2019 e 2023'])

if filtro == 'Raça':
    raca = st.selectbox(
        'Escolha a raça a analisar:',
        ['Preto', 'Pardo', 'Branco', 'Indígena', 'Amarelo', 'Não informado'])

botao = st.button('Exibir gráficos')  

if botao:
        caminho_arquivo = FILE_PATHS[ano]
        df = load_data(caminho_arquivo)
    except FileNotFoundError:
        st.error(f"ERRO: O arquivo **{caminho_arquivo}** não foi encontrado.")
        st.stop()
    except KeyError:
        st.error(f"Erro de configuração: O ano {ano} não está mapeado no FILE_PATHS.")
        st.stop()

    nota_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    NU_NOTA_GERAL = nota_cols.mean(axis=1)

    st.subheader(f"Resultados e Análise do ENEM {ano}")
    st.write(f"Total de participantes para a análise: **{len(df)}**")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Presença nas Provas")
        st.markdown("_Código 1 = Presente, 0 = Ausente_, 2 = Eliminado_")
        
        provas = {'Ciências da Natureza': 'TP_PRESENCA_CN', 
                  'Ciências Humanas': 'TP_PRESENCA_CH', 
                  'Linguagens e Códigos': 'TP_PRESENCA_LC', 
                  'Matemática': 'TP_PRESENCA_MT'}

        for nome, col_presenca in provas.items():
            if col_presenca in df_analise.columns:
                contagem = df[col_presenca].value_counts().reset_index()
                contagem.columns = ['Status', 'Total']
                
                st.markdown(f"**{nome}:**")
                # Exibe a contagem de presentes
                presentes = contagem[contagem['Status'] == 1]['Total'].sum()
                st.metric("Presentes", f"{presentes:,}".replace(',', '.'))
                #st.dataframe(contagem) # Opcional: mostrar a tabela completa

    # COLUNA 2: Gráfico da Média de Notas
    with col2:
