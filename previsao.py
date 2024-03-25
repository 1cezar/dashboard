import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns  
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objects as go


def previsao():          
    data = pd.read_csv('./Dados/Dados_Sudeste-Centro-Oeste_mensal.csv')
    data['DATA'] = pd.to_datetime(data['DATA'])
    correlation_matrix = data.corr(method='pearson')

    

    st.title("Análise de Dados de Energia")

    st.markdown("""
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    """, unsafe_allow_html=True)
    
    # Layout do gráfico
    col1, col2 = st.columns([10, 1])

    with col2:
        prazo = st.radio("Prazo:", ("Trimestral", "Longo prazo"), key='prazo')

    # Determinar a variável base com base na seleção do interruptor
    if prazo == "Trimestral":
        base_variable = "MPC_SECO"
        selected_label = "Trimestral"
    else:
        base_variable = "LPC_SECO"
        selected_label = "Longo prazo"

    # Criar um dicionário de mapeamento de variáveis
    variavel_map = {
        "Carga": "CE_SECO",
        "Custo Marginal de Operação":"CMO_SECO",
        "Energia Armazenada": "EA_SECO",
        "Geração de Energia": "GE_SECO",
        "Demanda Máxima": "DM_SECO",
        "Preço da Liquidação das Diferenças": "PLD_SECO",
        "Capacidade Instalada": "CI_SECO",
        "PIB": "PIB",
        # Adicione mais mapeamentos conforme necessário
    }

    # Dropdown para selecionar a variável para correlacionar com a variável base
    with col1:
        selected_variable = st.selectbox(f"Selecionar variável para correlacionar com {selected_label}:", list(variavel_map.keys()), index=1)


    # Verificar se uma variável foi selecionada
    if selected_variable:
        # Obter o nome da variável correspondente
        selected_variable_corresponding = variavel_map[selected_variable]

        # Adicionar variável base à seleção
        selected_variables = [selected_variable_corresponding, base_variable]

        # Filtrar os dados para incluir apenas as variáveis selecionadas
        filtered_data = data[['DATA'] + selected_variables]

        preco = ["Custo Marginal de Operação", "PIB", "Preço da Liquidação das Diferenças", "LPC_SECO", "MPC_SECO" ]

        if selected_variable in preco:
            grandesa = 'VALOR (R$)' 

        else:
            grandesa = 'VALOR (MW)'
            # Gráfico de série temporal para as variáveis selecionadas
        fig_time_series = px.line(filtered_data, x='DATA', y=selected_variables, 
                                title=f"Série Temporal das Variáveis Selecionadas para {selected_label}", 
                                labels={'variable': 'Variável', 'value': grandesa}, template='plotly_white')

        # Definir as cores das linhas
        fig_time_series.update_traces(line=dict(color='#1564c0'))  # Cor da primeira linha
        if len(selected_variables) > 1:
            fig_time_series.update_traces(line=dict(color='#90ff00'), selector=dict(name=selected_variables[1]))  # Cor da segunda linha, se houver

        # Adicionar eixo y à direita
        for i in range(1, len(selected_variables)):
            fig_time_series.update_traces(yaxis=f"y{i + 1}", selector=dict(name=selected_variables[i]))

        # Atualizar layout para incluir segundo eixo y à direita
        for i in range(2, len(selected_variables) + 1):
            fig_time_series.update_layout(yaxis2=dict(anchor='x', overlaying='y', side='right', position=0.95 - 0.04 * (i - 1), tickfont=dict(color='white'), title="($ꓤ) ꓤOꓶⱯꓥ"), showlegend=True)

        # Calcular e exibir a correlação de Pearson entre as variáveis selecionadas e a variável base
        for variable in selected_variables:
            if variable != base_variable:
                correlation_value = correlation_matrix.loc[base_variable, variable]

        formatted_correlation = "{:.8f}".format(correlation_value)

        st.metric(label="Correlação", value= formatted_correlation)

        st.plotly_chart(fig_time_series, use_container_width=True)
