import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns  
import matplotlib.pyplot as plt 
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from pyvis.network import Network
import tempfile
import webbrowser
import json

def load_inference_data(file_path):
    with open(file_path, 'r') as file:
        inference_data = json.load(file)
    return inference_data

def create_bar_chart(data, month, variable):
    values = [data[year][month][variable] for year in data]
    years = list(data.keys())
    
    fig = go.Figure(data=[
        go.Bar(x=years, y=values)
    ])
    
    fig.update_layout(title=f'Inferência Bayesiana - {variable} - {month}', xaxis_title='Ano', yaxis_title='Valor')
    
    return fig

topology_data = {
    "name": "ind_003",
    "topologia": [
        ["LPC_SECO", "CMO_SECO"],
        ["LPC_SECO", "GE_SECO"],
        ["LPC_SECO", "CE_SECO"],
        ["LPC_SECO", "PLD_SECO"],
        ["CMO_SECO", "PLD_SECO"],
        ["CMO_SECO", "CE_SECO"],
        ["CMO_SECO", "GE_SECO"],
        ["GE_SECO", "CE_SECO"],
        ["GE_SECO", "PLD_SECO"],
        ["PLD_SECO", "CE_SECO"]
    ],
    "target_variable": "{alvo}"
}


def render_dag(topology_data):
    # Criar um grafo direcionado acíclico (DAG)
    G = nx.DiGraph()

    # Adicionar nós e arestas ao grafo
    for edge in topology_data["topologia"]:
        G.add_edge(edge[0], edge[1])

    # Layout do grafo
    pos = nx.spring_layout(G, dim=3, seed=41)  # Layout usando algoritmo Spring em 3D

    # Criar os nós do grafo
    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes:
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    # Criar as arestas do grafo
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    # Criar a figura
    fig = go.Figure()

    # Adicionar arestas à figura
    fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='gray', width=0.5), hoverinfo='none'))

    # Adicionar nós à figura
    fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='text', text=list(G.nodes()), textposition="middle center", marker=dict(color="crimson", size=30)))

    # Configurar layout da figura
    fig.update_layout(title=f"Topologia: {topology_data['name']}", titlefont_size=12, showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40), annotations=[ dict(text="Python code: <a href='https://plotly.com/python/'> https://plotly.com/python/</a>", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ], scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    frames = []
    for i in np.linspace(0, 2 * np.pi, 36):
        new_x = np.cos(i) * np.array(node_x) - np.sin(i) * np.array(node_y)
        new_y = np.sin(i) * np.array(node_x) + np.cos(i) * np.array(node_y)
        frames.append(go.Frame(data=[go.Scatter3d(x=new_x, y=new_y, z=node_z, mode='markers+text', text=list(G.nodes()), textposition="middle center", marker=dict(color="skyblue", size=15))]))

    fig.frames = frames

    # Exibir a figura
    st.plotly_chart(fig)
