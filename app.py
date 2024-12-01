import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import polars as pl
from PIL import Image
import plotly.express as px
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

st.set_page_config(page_title="SpeechGraph", page_icon='🐿️', layout='wide')

def bigram_edges(tokens):
    edgetable = list(zip(tokens[:-1], tokens[1:]))
    return edgetable

def ReadTextExample():
  path_text = 'example.txt'
  text_w2v = []
  for line in open(path_text): 
    if line!='\n':
        text_w2v.append(line)
  text = ''.join(text_w2v)
#   text = re.split(r'\n', text)
  return text

def Token2Graph(edges_token):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges_token)
    return G

def PlotGraph(tokens):
	edges_token = bigram_edges(tokens)
	G = Token2Graph(edges_token)

	fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño ajustado
	pos = nx.spring_layout(G, seed=42)  # Disposición de nodos
	nx.draw(
		G,
		pos,
		with_labels=True,
		node_color='red',
		node_size=12,
		edge_color='gray',
		font_size=10,
		ax=ax
	)

	st.title("Speech Graph")
	st.pyplot(fig)

from vis_utils import Network as Net

keywords_nodes = []

viskargs = dict(
    height="1050px", 
    width="100%", 
    bgcolor="white", 
    keyword_color = "#FF0000",
    # node_color="#4682B4", 
    node_color="#FF0000", 
    font_color="#222222", 
    key_weight=1.2,
    font_size=30,
    node_size=18,
    edge_width=2,
    directed=True, 
    ifplot=False,
    heading="",
)

def read_html():
	html_file = "textgraph.html"  
	try:
		with open(html_file, "r", encoding="utf-8") as file:
			html_content = file.read()
		components.html(html_content, height=900, scrolling=True)
	except FileNotFoundError:
		st.error("El archivo HTML no se encontró. Verifica la ruta.")

def main():
	st.title('Speech Directed MultiGraph (Co-occurrence network)')

	with st.container():
		st.header('Demo')

		txt_example = ReadTextExample()

		text_sample = re.split(r'\n', txt_example)[:10] + ['...']
		text_sample = '\n'.join(text_sample)
		st.text('Archivo de texto preprocesado para generar un grafo que refleje la co-ocurrencia (links) de palabras (nodos) en un documento de texto que describe un caso clínico de depresión del manual DSM-V')
		st.text(text_sample)

		st.download_button(
			label="Descargar",
			data=txt_example,
			file_name='example.txt',
			icon='📄',
			mime='text/plain'
		)
		st.write('---')

	with st.container():
		st.header('Vizualizar Grafo')
		# txt_file = st.file_uploader("Upload .txt file with words sequence:", type=['txt'])
		txt_file = st.file_uploader("Carga un archivo .txt que contenga una palabra por línea de texto.", type=['txt'])
		
		if txt_file is not None:
			info_text = {
				"name": txt_file.name,
				"type": txt_file.type,
				"size": txt_file.size
			}
			if info_text['type']=='text/plain':
				txt = str(txt_file.read(), 'utf-8')
				tokens = re.split(r'\n', txt)
				# st.text(tokens)
				# st.text(txt)
				edges_token = bigram_edges(tokens)
				G = Token2Graph(edges_token)
				nt = Net(keywords_nodes = keywords_nodes,**viskargs)
				nt.from_nx(G)
				nt.options.edges.color = "#000000"

				nt.save_graph("textgraph.html")
				text = ' '.join(tokens)
				read_html()
				# st.write(txt)


if __name__ == '__main__':
	main()