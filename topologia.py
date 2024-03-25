import streamlit as st
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns  
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objects as go
import networkx as nx
import json

def topologia():
        st.title("Topologia")
        # data = pd.read_csv('./Dados/Dados_Sudeste-Centro-Oeste_mensal.csv')
        # data['DATA'] = pd.to_datetime(data['DATA'])
        # correlation_matrix = data.corr(method='pearson')

        # results = pd.read_csv('./Dados/resultados_previsao_3_anos_INf_HI_PLD_AE.csv')
        # results = results.drop(columns=['LPC_SECO'])
        # results['Data'] = pd.to_datetime(results.index)
        # results.set_index('Data', inplace=True)

        # data_serie_adicional = data[['DATA', 'LPC_SECO']]

        # data_serie_adicional['DATA'] = pd.to_datetime(data_serie_adicional['DATA'])
        # data_serie_adicional.set_index('DATA', inplace=True)

        # def load_inference_data(file_path):
        #     with open(file_path, 'r') as file:
        #         inference_data = json.load(file)
        #     return inference_data

        # inference_data = load_inference_data('./Dados/ind_006.json')
        # st.title("Topologia")
        # fig = go.Figure()

        # # Adicionar a série adicional ao gráfico
        # fig.add_trace(go.Scatter(x=data_serie_adicional.index, y=data_serie_adicional['LPC_SECO'], mode='lines', name='Série Adicional'))

        # # Adicionar os dados de previsão ao gráfico
        # for col in results.columns:
        #     if col != 'Data':
        #         fig.add_trace(go.Scatter(x=results.index, y=results[col], mode='lines', name=col))

        # # Configurar o layout do gráfico
        # fig.update_layout(title='Previsão LPC_SECO e Série Adicional',
        #                 xaxis_title='Data',
        #                 yaxis_title='Valor',               
        #                 legend_orientation='h',
        #                 legend_y=1.1,
        #                 legend_x=0.0,
        #                 colorway=px.colors.qualitative.Light24)

        # # Exibir o gráfico
        # st.plotly_chart(fig)
        # # Criar um grafo direcionado acíclico (DAG)
        # G = nx.DiGraph()

        # # Adicionar nós e arestas ao grafo
        # for edge in topology_data["topologia"]:
        #     G.add_edge(edge[0], edge[1])

        # # Layout do grafo
        # pos = nx.spring_layout(G, dim=3, seed=41)  # Layout usando algoritmo Spring em 3D

        # # Criar os nós do grafo
        # node_x = []
        # node_y = []
        # node_z = []
        # for node in G.nodes:
        #     x, y, z = pos[node]
        #     node_x.append(x)
        #     node_y.append(y)
        #     node_z.append(z)

        # # Criar as arestas do grafo
        # edge_x = []
        # edge_y = []
        # edge_z = []
        # for edge in G.edges():
        #     x0, y0, z0 = pos[edge[0]]
        #     x1, y1, z1 = pos[edge[1]]
        #     edge_x.extend([x0, x1, None])
        #     edge_y.extend([y0, y1, None])
        #     edge_z.extend([z0, z1, None])

        # # Criar a figura
        # fig = go.Figure()

        # # Adicionar arestas à figura
        # fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='gray', width=0.5), hoverinfo='none'))

        # # Adicionar nós à figura
        # fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='text', text=list(G.nodes()), textposition="middle center", marker=dict(color="crimson", size=30)))

        # # Configurar layout da figura
        # fig.update_layout(title=f"Topologia: {topology_data['name']}", titlefont_size=12, showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40), annotations=[ dict(text="Python code: <a href='https://plotly.com/python/'> https://plotly.com/python/</a>", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ], scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        # frames = []
        # for i in np.linspace(0, 2 * np.pi, 36):
        #     new_x = np.cos(i) * np.array(node_x) - np.sin(i) * np.array(node_y)
        #     new_y = np.sin(i) * np.array(node_x) + np.cos(i) * np.array(node_y)
        #     frames.append(go.Frame(data=[go.Scatter3d(x=new_x, y=new_y, z=node_z, mode='markers+text', text=list(G.nodes()), textposition="middle center", marker=dict(color="skyblue", size=15))]))

        # fig.frames = frames

        # # Exibir a figura
        # st.plotly_chart(fig)

    