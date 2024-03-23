import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns  
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

data = pd.read_csv('./Dados_Sudeste-Centro-Oeste_mensal.csv')
data['DATA'] = pd.to_datetime(data['DATA'])

# Calcular correlações usando o método de Pearson
correlation_matrix = data.corr(method='pearson')

# Configurações de estilo
st.set_page_config(
    page_title="Análise de Dados de Energia",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Layout do aplicativo
st.title("Análise de Dados de Energia")

# Layout do gráfico
col1, col2 = st.columns([1, 8])
with col1:
    prazo = st.radio("Prazo:", ("Trimestral", "Longo prazo"))

# Determinar a variável base com base na seleção do interruptor
if prazo == "Trimestral":
    base_variable = "MPC_SECO"
    selected_label = "Trimestral"
else:
    base_variable = "LPC_SECO"
    selected_label = "Longo prazo"

# Dropdown para selecionar as variáveis para correlacionar com a variável base
with col2:
    selected_variables = st.multiselect(f"Selecionar variáveis para correlacionar com {selected_label}:", data.columns[1:], default=[data.columns[2]])

# Verificar se alguma variável foi selecionada
if selected_variables:
    # Adicionar variável base à seleção
    selected_variables.append(base_variable)

    # Filtrar os dados para incluir apenas as variáveis selecionadas
    filtered_data = data[['DATA'] + selected_variables]

    # Gráfico de série temporal para as variáveis selecionadas
    fig_time_series = px.line(filtered_data, x='DATA', y=selected_variables, 
                              title=f"Série Temporal das Variáveis Selecionadas para {selected_label}", 
                              labels={'variable': 'Variável', 'value': 'Valor (MW)'}, template='plotly_white')

    # Adicionar eixo y à direita
    for i in range(1, len(selected_variables)):
        fig_time_series.update_traces(yaxis=f"y{i + 1}", selector=dict(name=selected_variables[i]))

    # Atualizar layout para incluir segundo eixo y à direita
    for i in range(2, len(selected_variables) + 1):
        fig_time_series.update_layout(yaxis2=dict(anchor='x', overlaying='y', side='right', position=0.95 - 0.05 * (i - 1)), showlegend=True)
    
    # Calcular e exibir a correlação de Pearson entre as variáveis selecionadas e a variável base
    for variable in selected_variables:
        if variable != base_variable:
            correlation_value = correlation_matrix.loc[base_variable, variable]
            # Adicionar botões de alternância dentro do gráfico
            fig_time_series.add_annotation(
                x=0.5,
                y=1.0,
                opacity=0.8,
                xref="paper",
                yref="paper",
                text=f"Correlação: {correlation_value:.2f}",
                showarrow=False,
                bgcolor="Green" if correlation_value >= 0.0 else "Red",
                font=dict(size=25, color="white", family="monospace"),
            )

    st.plotly_chart(fig_time_series, use_container_width=True)
   

    # Definir o código JavaScript
    javascript_code = """
    <h2>Exemplo de Integração JavaScript</h2>
    <p>Clique no botão abaixo para exibir um alerta em JavaScript.</p>
    <button onclick="showAlert()">Mostrar Alerta</button>

    <script>
        function showAlert() {
            alert("Este é um alerta em JavaScript!");
        }
    </script>
    """

    # Renderizar o componente de JavaScript
    components.html(javascript_code)
