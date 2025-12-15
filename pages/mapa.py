import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json
import json

@st.cache_data
def load_geojson(path):
    # Certifique-se de que o arquivo 'municipios_ibge.geojson.json' está no mesmo diretório
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
geojson_municipios = load_geojson('municipios_ibge.geojson.json')

#Grafico de mapa

