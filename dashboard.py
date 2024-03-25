import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from previsao import previsao
from topologia import topologia
from demanda import demanda

st.set_page_config(layout="wide", page_icon=None)

paginas = option_menu(None, ["Análise de Variáveis", "Curva Forward"], 
    icons=['bi bi-search', 'bi bi-graph-up','bi bi-clipboard-pulse'], 
    menu_icon="cast",
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "width": "10"},
        "nav-link-selected": {"background-color": "#398e3d"},
    })

if paginas == "Análise de Variáveis":
    previsao()

if paginas == "Curva Forward":
    topologia()

