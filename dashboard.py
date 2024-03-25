import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from previsao import previsao
from topologia import topologia

st.set_page_config(layout="wide")

paginas = option_menu(None, ["Previsão", "Topologia"], 
    icons=['bi bi-graph-up', 'bi bi-bezier2'], 
    menu_icon="cast",
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "width": "10"},
        "nav-link-selected": {"background-color": "#398e3d"},
    })

if paginas == "Previsão":
    previsao()

else:
    topologia()
