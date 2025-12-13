import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. Dicionários de Caminhos e Mapeamento ---
FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_AMOSTRA.csv',
    '2021': 'ENEM_2021_FILTRADO_AMOSTRA.csv',
    '2022': 'ENEM_2022_FILTRADO_AMOSTRA.csv',
    '2023': 'ENEM_2023_FILTRADO_AMOSTRA.csv'
}

# Dicionários de Mapeamento (Códigos ENEM -> Texto)
MAPPING_Q006 = {
    'A': 'Até 1 salário mínimo', 'B': 'Até 1 salário mínimo',
    'C': 'Entre 1 e 3 salários mínimos', 'D': 'Entre 1 e 3 salários mínimos', 
    'E': 'Entre 3 e 6 salários mínimos', 'F': 'Entre 3 e 6 salários mínimos', 
    'G': 'Acima de 6 salários mínimos', 'H': 'Acima de 6 salários mínimos',
    'I': 'Acima de 6 salários mínimos', 'J': 'Acima de 6 salários mínimos',
    'K': 'Acima de 6 salários mínimos', 'L': 'Acima de 6 salários mínimos',
    'M': 'Acima de 6 salários mínimos', 'N': 'Acima de 6 salários mínimos',
    'O': 'Acima de 6 salários mínimos', 'P': 'Acima de 6 salários mínimos', 
    'Q': 'Acima de 6 salários mínimos', 
}

MAPPING_CONCLUSAO = {
    1: 'Entre 2007 e 2012', 2: 'Entre 2007 e 2012', 3: 'Entre 2007 e 2012', 
    4: 'Entre 2007 e 2012', 5: 'Entre 2007 e 2012', 6: 'Entre 2007 e 2012', 
    7: 'Entre 2013 e 2018', 8: 'Entre 2013 e 2018', 9: 'Entre 2013 e 2018', 
    10: 'Entre 2013 e 2018', 11: 'Entre 2013 e 2018', 12: 'Entre 2013 e 2018', 
    13: 'Entre 2019 e 2023', 14: 'Entre 2019 e 2023', 15: 'Entre 2019 e 2023',
    16: 'Entre 2019 e 2023', 17: 'Entre 2019 e 2023', 18: 'Entre 2019 e 2023',
}

MAPPING_RACA = {
    1: 'Branco', 2: 'Preto', 3: 'Pardo', 4: 'Amarelo', 5: 'Indígena', 0: 'Não informado'
}

# --- 3. Funções de Dados ---

@st.cache_data
def load_data(path):
    """Carrega o CSV e retorna o DataFrame bruto."""
    df = pd.read_csv(path, sep=';', encoding='latin1')
    return df

@st.cache_data
def preprocess_data(df):
    """Aplica o mapeamento para criar colunas legíveis."""
    df_processed = df.copy()

    # Aplica mapeamentos
    df_processed['FAIXA_SALARIAL'] = df_processed['Q006'].astype(str).map(MAPPING_Q006).fillna('Outros')
    df_processed['PERIODO_CONCLUSAO'] = df_processed['TP_ANO_CONCLUIU'].map(MAPPING_CONCLUSAO).fillna('Não informado')
    df_processed['RACA_NOME'] = df_processed['TP_COR_RACA'].map(MAPPING_RACA).fillna('Não informado')
    
    # Garante que colunas de notas sejam float
    nota_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    for col in nota_cols:
        df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
    return df_processed

# --- 4. INTERFACE DO USUÁRIO ---
st.title('Dashboard das notas do Enem nos últimos anos 📊')
st.header('Filtros:')

# Variáveis do Streamlit
ano = st.selectbox('Escolha o ano para a análise:', ('2020', '2021', '2022', '2023'))
filtro = st.selectbox('Escolha uma variável para análise:', sorted(['Renda', 'Ano de conclusão', 'Raça']))

salario = None
if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Até 1 salário mínimo', 'Entre 1 e 3 salários mínimos', 'Entre 3 e 6 salários mínimos', 'Acima de 6 salários mínimos'])

ano_c = None
if filtro == 'Ano de conclusão':
    ano_c = st.selectbox(
        'Escolha o período do ano de conclusão:',
        ['Entre 2007 e 2012', 'Entre 2013 e 2018', 'Entre 2019 e 2023'])

raca = None
if filtro == 'Raça':
    raca = st.selectbox(
        'Escolha a raça a analisar:',
        ['Preto', 'Pardo', 'Branco', 'Indígena', 'Amarelo', 'Não informado'])

botao = st.button('Exibir gráficos')

# --- 5. LÓGICA DE EXECUÇÃO E GRÁFICOS ---
if botao:
    st.subheader(f"Processando Dados do ENEM {ano}")
    
    # 5.1. Carregamento Bruto e Mapeamento
    try:
        caminho_arquivo = FILE_PATHS[ano]
        df_bruto = load_data(caminho_arquivo)
    except FileNotFoundError:
        st.error(f"ERRO: O arquivo **{caminho_arquivo}** não foi encontrado.")
        st.stop()
    except KeyError:
        st.error(f"Erro de configuração: O ano {ano} não está mapeado no FILE_PATHS.")
        st.stop()

    df_base = preprocess_data(df_bruto)
    
    # 5.2. Aplicação da Filtragem (CRUCIAL PARA O DASHBOARD)
    df_filtrado = df_base.copy()
    
    if filtro == 'Renda' and salario is not None:
        df_filtrado = df_filtrado[df_filtrado['FAIXA_SALARIAL'] == salario]
        st.info(f"Filtro ativo: Renda = **{salario}**")

    elif filtro == 'Ano de conclusão' and ano_c is not None:
        df_filtrado = df_filtrado[df_filtrado['PERIODO_CONCLUSAO'] == ano_c]
        st.info(f"Filtro ativo: Ano de Conclusão = **{ano_c}**")

    elif filtro == 'Raça' and raca is not None:
        df_filtrado = df_filtrado[df_filtrado['RACA_NOME'] == raca]
        st.info(f"Filtro ativo: Raça = **{raca}**")

    # 5.3. Finalização da Análise (df_analise)
    nota_cols = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    
    # Calcula a média e remove linhas com notas NaN (apenas para análise)
    df_filtrado['NU_NOTA_GERAL'] = df_filtrado[nota_cols].mean(axis=1)
    df_analise = df_filtrado.dropna(subset=['NU_NOTA_GERAL'])
    
    if len(df_analise) == 0:
        st.warning("Nenhum participante com notas válidas encontrado com os filtros selecionados.")
        st.stop()

    st.subheader(f"Resultados e Análise do ENEM {ano}")
    st.write(f"Total de participantes para a análise: **{len(df_analise)}**")

    col1, col2 = st.columns([1, 2])

    # COLUNA 1: Métricas de Presença
    with col1:
        st.markdown("#### Presença nas Provas")
        st.markdown("_Código 1 = Presente, 0 = Ausente, 2 = Eliminado_")
        
        provas = {'Ciências da Natureza': 'TP_PRESENCA_CN', 
                  'Ciências Humanas': 'TP_PRESENCA_CH', 
                  'Linguagens e Códigos': 'TP_PRESENCA_LC', 
                  'Matemática': 'TP_PRESENCA_MT'}

        for nome, col_presenca in provas.items():
            if col_presenca in df_analise.columns:
                # Usa df_analise (que contém apenas participantes com notas válidas)
                contagem = df_analise[col_presenca].value_counts().reset_index()
                contagem.columns = ['Status', 'Total']
                
                st.markdown(f"**{nome}:**")
                # Exibe a contagem de presentes (Status == 1)
                presentes = contagem[contagem['Status'] == 1]['Total'].sum()
                st.metric("Presentes", f"{presentes:,}".replace(',', '.'))


    # COLUNA 2: Gráfico da Média de Notas
    with col2:
        st.markdown("#### Média Geral de Notas (Ajustada)")
        
        media_geral = df_analise['NU_NOTA_GERAL'].mean()
        
        df_grafico_media = pd.DataFrame({
            'Ano': [ano],
            'Média Geral': [media_geral]
        })
        
        # Cria o gráfico de barras
        fig_media = px.bar(
            df_grafico_media,
            x='Ano',
            y='Média Geral',
            text='Média Geral',
            title=f'Média Geral de Notas (ENEM {ano})',
            color='Ano',
            color_discrete_sequence=['#1f77b4']
        )
        
        fig_media.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        fig_media.update_layout(yaxis_range=[350, 650])

        st.plotly_chart(fig_media, use_container_width=True)
