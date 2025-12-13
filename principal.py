import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Dashboard das notas do Enem nos últimos anos",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# AJUSTE: Seus caminhos precisam ser absolutos se estiver rodando o Streamlit fora da pasta dos arquivos.
# Exemplo se os arquivos estiverem no mesmo diretório:
FILE_PATHS = {
    '2020': 'ENEM_2020_FILTRADO_AMOSTRA.csv',
    '2021': 'ENEM_2021_FILTRADO_AMOSTRA.csv',
    '2022': 'ENEM_2022_FILTRADO_AMOSTRA.csv',
    '2023': 'ENEM_2023_FILTRADO_AMOSTRA.csv'
}

@st.cache_data
def load_data(path):
    # Usando o caminho no cache para garantir que carregue o arquivo certo
    df = pd.read_csv(path, sep=';', encoding='latin1')
    
    # Mapeamentos
    mapeamento = {
        'Q006': {
            'A': 'Até R$1.420', 'B': 'Até R$1.420', 'C': 'Entre R$1.420 e R$3.530', 
            'D': 'Entre R$1.420 e R$3.530', 'E': 'Entre R$3.531 e R$9.884', 
            'F': 'Entre R$3.531 e R$9.884', 'G': 'Acima de R$9.884',
        },
        'TP_ANO_CONCLUIU': {
            1: 'Entre 2007 e 2012', 2: 'Entre 2007 e 2012', 3: 'Entre 2007 e 2012', 
            4: 'Entre 2007 e 2012', 5: 'Entre 2007 e 2012', 6: 'Entre 2007 e 2012', 
            7: 'Entre 2013 e 2018', 8: 'Entre 2013 e 2018', 9: 'Entre 2013 e 2018', 
            10: 'Entre 2013 e 2018', 11: 'Entre 2013 e 2018', 12: 'Entre 2013 e 2018', 
            13: 'Entre 2019 e 2023', 14: 'Entre 2019 e 2023', 15: 'Entre 2019 e 2023',
            16: 'Entre 2019 e 2023', 17: 'Entre 2019 e 2023', 18: 'Entre 2019 e 2023',
        },
        'TP_COR_RACA': {
            1: 'Branco', 2: 'Preto', 3: 'Pardo', 4: 'Amarelo', 5: 'Indígena', 0: 'Não informado'
        }
    }
    
    # Aplica mapeamentos
    df['FAIXA_SALARIAL'] = df['Q006'].astype(str).map(mapeamento['Q006']).fillna('Outros')
    df['PERIODO_CONCLUSAO'] = df['TP_ANO_CONCLUIU'].map(mapeamento['TP_ANO_CONCLUIU']).fillna('Não informado')
    df['RACA_NOME'] = df['TP_COR_RACA'].map(mapeamento['TP_COR_RACA']).fillna('Não informado')
    
    return df

st.title('Dashboard das notas do Enem nos últimos anos 📊')
st.header('Filtros:')

# Variáveis do Streamlit
ano = st.selectbox('Escolha o ano para a análise:', ('2020', '2021', '2022', '2023'))
filtro = st.selectbox('Escolha uma variável para análise:', sorted(['Renda', 'Ano de conclusão', 'Raça']))

salario = None
if filtro == 'Renda':
    salario = st.selectbox(
        'Escolha a faixa salarial:',
        ['Até R$1.420', 'Entre R$1.420 e R$3.530', 'Entre R$3.531 e R$9.884', 'Acima de R$9.884'])

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

if botao:
    st.subheader(f"Carregando e Filtrando Dados do ENEM {ano}")
    
    # --- 1. Carregamento dos Dados (Corrigido o nome da variável) ---
    try:
        caminho_arquivo = FILE_PATHS[ano] # Usa o valor 'ano' do selectbox
        df_base = load_data(caminho_arquivo)
        st.success(f"Dados do ENEM {ano} carregados com sucesso! ({len(df_base)} linhas)")
        
    except KeyError:
        st.error(f"Erro de configuração: O ano {ano} não está definido na variável FILE_PATHS.")
        st.stop()
    except FileNotFoundError:
        st.error(f"ERRO DE ARQUIVO: O arquivo **{caminho_arquivo}** não foi encontrado. Por favor, verifique o caminho no seu ambiente de execução.")
        st.stop()
    
    # --- 2. Aplicação do Filtro nos Dados Carregados ---
    
    df_filtrado = df_base.copy()
    filtro_aplicado = False

    if filtro == 'Renda' and salario is not None:
        df_filtrado = df_filtrado[df_filtrado['FAIXA_SALARIAL'] == salario]
        filtro_aplicado = True
        st.info(f"Filtro ativo: Renda = **{salario}**")

    elif filtro == 'Ano de conclusão' and ano_c is not None:
        df_filtrado = df_filtrado[df_filtrado['PERIODO_CONCLUSAO'] == ano_c]
        filtro_aplicado = True
        st.info(f"Filtro ativo: Ano de Conclusão = **{ano_c}**")

    elif filtro == 'Raça' and raca is not None:
        df_filtrado = df_filtrado[df_filtrado['RACA_NOME'] == raca]
        filtro_aplicado = True
        st.info(f"Filtro ativo: Raça = **{raca}**")

    # --- 3. Resultado do Teste ---
    
    st.subheader("Resultado da Filtragem:")
    st.write(f"Linhas restantes após filtro: **{len(df_filtrado)}**")
    
    if len(df_filtrado) > 0:
        st.dataframe(df_filtrado.head())
    else:
        st.warning("Nenhuma linha corresponde ao filtro selecionado.")
