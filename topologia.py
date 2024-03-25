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
import altair as alt
from streamlit_option_menu import option_menu

def topologia():
        cenario = option_menu(None, ["Cenário Um", "Cenário Dois", "Cenário Três"], 
        icons=['bi bi-tv', 'bi bi-tv','bi bi-tv'], 
        menu_icon="cast",
        default_index=0, 
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "wigth": "10px"},
            "nav-link-selected": {"background-color": "#1564c0"},
        })
        data = pd.read_csv('./Dados/Dados_Sudeste-Centro-Oeste_mensal.csv')
        data['DATA'] = pd.to_datetime(data['DATA'])

        data_limite = data.loc[data['DATA'] <= '2021-12-01']

        results = pd.read_csv('./Dados/resultados_previsao_3_anos_INf_HI_PLD_AE.csv')
        results['Data'] = pd.to_datetime(results['Data'])

        results2 = pd.read_csv('./Dados/resultados/resultados/preco/Expe_2/resultados_previsao_3_anos_2_exper.csv')
        results2['Data'] = pd.to_datetime(results2['Data'])

        results3 = pd.read_csv('./Dados/resultados/resultados/preco/Expe_3_melhor/resultados_previsao_3_anos_INf_HI_PLD_AE.csv')
        results3['Data'] = pd.to_datetime(results3['Data'])


        def load_inference_data(file_path):
            with open(file_path, 'r') as file:
                inference_data = json.load(file)
            return inference_data

        topology_data = load_inference_data('./Dados/ind_006.json')
        topology_data2 = load_inference_data('./Dados/resultados/resultados/preco/Expe_2/ind_005.json')

        if cenario == "Cenário Um":

            c1, c2= st.columns(2)

            with st.container():
                c1.write("")
                c2.write("")

            with c2:
                G = nx.DiGraph()

                # # Adicionar nós e arestas ao grafo
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

                # # Adicionar arestas à figura
                fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='limegreen', width=0.8), hoverinfo='none'))

                # Adicionar nós à figura
                fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=list(G.nodes()), 
                                        textposition="middle center", marker=dict(color='limegreen', size=40)))

                # # Configurar layout da figura
                fig.update_layout(title=f"Topologia: {topology_data['name']}", titlefont_size=12, showlegend=False, hovermode='closest', 
                                margin=dict(b=20,l=5,r=5,t=40), 
                                annotations=[ dict(text="", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ], scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

                frames = []
                for i in np.linspace(0, 2 * np.pi, 36):
                    new_x = np.cos(i) * np.array(node_x) - np.sin(i) * np.array(node_y)
                    new_y = np.sin(i) * np.array(node_x) + np.cos(i) * np.array(node_y)
                    frames.append(go.Frame(data=[go.Scatter3d(x=new_x, y=new_y, z=node_z, mode='markers+text', text=list(G.nodes()), textposition="middle center", marker=dict(color="skyblue", size=15))]))

                fig.frames = frames

                # Exibir a figura
                st.plotly_chart(fig)
                
            with c1:
                st.markdown("### Where can I get some?")
                st.markdown("There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures")

            '''
            confidence_factor = 0.3
            results['lower_lim'] = results['mean'] - ((results['mean'] - results['lower_lim']) * confidence_factor)
            results['upper_lim'] = results['mean'] + ((results['upper_lim'] - results['mean']) * confidence_factor) '''   
            fig = go.Figure()
            data_limite = data.loc[data['DATA'] <= '2021-12-01']
            # Adicionar a linha média
            fig.add_trace(go.Scatter(x=data_limite['DATA'], y=data_limite['LPC_SECO'], mode='lines', name='Real'))

            # Adicionar os limites superior e inferior
            fig.add_trace(go.Scatter(x=results['Data'], y=results['upper_lim'], mode='lines', 
                                        line=dict(color='rgba(0,0,0,0)', width=1),
                                    showlegend=False))
            fig.add_trace(go.Scatter(x=results['Data'], y=results['lower_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Inferior'))
            fig.add_trace(go.Scatter(x=results['Data'], y=results['upper_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Superior'))
            fig.add_trace(go.Scatter(x=results['Data'], y=results['mean'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Previsto'))

            fig.update_layout(title='Intervalo de Confiança',
                            xaxis_title='Data',
                            yaxis_title='Valor',
                            width=1275)
            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)

        if cenario == "Cenário Dois":
            c3, c4= st.columns(2)
            
            with c3:
                st.markdown("### Where can I get some?")
                st.markdown("There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures")
            with c4:
                G = nx.DiGraph()

                # # Adicionar nós e arestas ao grafo
                for edge in topology_data2["topologia"]:
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

                # # Adicionar arestas à figura
                fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='limegreen', width=0.8), hoverinfo='none'))

                # Adicionar nós à figura
                fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=list(G.nodes()), 
                                        textposition="middle center", marker=dict(color='limegreen', size=40)))

                # # Configurar layout da figura
                fig.update_layout(title=f"Topologia: {topology_data['name']}", titlefont_size=12, showlegend=False, hovermode='closest', 
                                margin=dict(b=20,l=5,r=5,t=40), 
                                annotations=[ dict(text="", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ], scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

                frames = []
                for i in np.linspace(0, 2 * np.pi, 36):
                    new_x = np.cos(i) * np.array(node_x) - np.sin(i) * np.array(node_y)
                    new_y = np.sin(i) * np.array(node_x) + np.cos(i) * np.array(node_y)
                    frames.append(go.Frame(data=[go.Scatter3d(x=new_x, y=new_y, z=node_z, mode='markers+text', text=list(G.nodes()), textposition="middle center", marker=dict(color="skyblue", size=15))]))

                fig.frames = frames

                # Exibir a figura
                st.plotly_chart(fig)

            fig = go.Figure()
            # Adicionar a linha média
            fig.add_trace(go.Scatter(x=data_limite['DATA'], y=data_limite['LPC_SECO'], mode='lines', name='Real'))

            # Adicionar os limites superior e inferior
            fig.add_trace(go.Scatter(x=results2['Data'], y=results2['upper_lim'], mode='lines', 
                                        line=dict(color='rgba(0,0,0,0)', width=1),
                                    showlegend=False))
            fig.add_trace(go.Scatter(x=results2['Data'], y=results2['lower_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Inferior'))
            fig.add_trace(go.Scatter(x=results2['Data'], y=results2['upper_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Superior'))
            fig.add_trace(go.Scatter(x=results2['Data'], y=results2['mean'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Previsto'))

            fig.update_layout(title='Intervalo de Confiança',
                            xaxis_title='Data',
                            yaxis_title='Valor',
                            width=1275)
            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)

        if cenario == "Cenário Três":
            c1, c2= st.columns(2)

            with st.container():
                c1.write("")
                c2.write("")

            with c2:
                G = nx.DiGraph()

                # # Adicionar nós e arestas ao grafo
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

                # # Adicionar arestas à figura
                fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='limegreen', width=0.8), hoverinfo='none'))

                # Adicionar nós à figura
                fig.add_trace(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=list(G.nodes()), 
                                        textposition="middle center", marker=dict(color='limegreen', size=40)))

                # # Configurar layout da figura
                fig.update_layout(title=f"Topologia: {topology_data['name']}", titlefont_size=12, showlegend=False, hovermode='closest', 
                                margin=dict(b=20,l=5,r=5,t=40), 
                                annotations=[ dict(text="", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ], scene=dict(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

                frames = []
                for i in np.linspace(0, 2 * np.pi, 36):
                    new_x = np.cos(i) * np.array(node_x) - np.sin(i) * np.array(node_y)
                    new_y = np.sin(i) * np.array(node_x) + np.cos(i) * np.array(node_y)
                    frames.append(go.Frame(data=[go.Scatter3d(x=new_x, y=new_y, z=node_z, mode='markers+text', text=list(G.nodes()), textposition="middle center", marker=dict(color="skyblue", size=15))]))

                fig.frames = frames

                # Exibir a figura
                st.plotly_chart(fig)
                
            with c1:
                st.markdown("### Where can I get some?")
                st.markdown("There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures")

            '''
            confidence_factor = 0.3
            results['lower_lim'] = results['mean'] - ((results['mean'] - results['lower_lim']) * confidence_factor)
            results['upper_lim'] = results['mean'] + ((results['upper_lim'] - results['mean']) * confidence_factor) '''   
            fig = go.Figure()
            data_limite = data.loc[data['DATA'] <= '2021-12-01']
            # Adicionar a linha média
            fig.add_trace(go.Scatter(x=data_limite['DATA'], y=data_limite['LPC_SECO'], mode='lines', name='Real'))

            # Adicionar os limites superior e inferior
            fig.add_trace(go.Scatter(x=results3['Data'], y=results3['upper_lim'], mode='lines', 
                                        line=dict(color='rgba(0,0,0,0)', width=1),
                                    showlegend=False))
            fig.add_trace(go.Scatter(x=results3['Data'], y=results3['lower_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Inferior'))
            fig.add_trace(go.Scatter(x=results3['Data'], y=results3['upper_lim'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Limite Superior'))
            fig.add_trace(go.Scatter(x=results3['Data'], y=results3['mean'], mode='lines', fill='tonexty', fillcolor='rgba(0,100,80,0.2)',
                                    name='Previsto'))

            fig.update_layout(title='Intervalo de Confiança',
                            xaxis_title='Data',
                            yaxis_title='Valor',
                            width=1275)
            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)