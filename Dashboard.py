import streamlit as st
import requests 
import urllib3
import pandas as pd
import plotly.express as px

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Desativamos a validação SSL porque o servidor está com certificado inválido.
# Isso permitiu que o Streamlit pegasse os dados normalmente.

def formata_numero(valor, prefixo = ''): 
    # Função para formatar números grandes em unidades mais legíveis.
    # Ex.: 1500 -> "1.50 mil", 2_000_000 -> "2.00 milhões"
    # 'valor' é o número que queremos formatar.
    # 'prefixo' permite adicionar símbolos como "R$" ou "%", mas aqui não é usado.
    for unidade in ['', 'mil']: # A ideia é verificar se o valor ainda é menor que 1000 antes de mudar para a próxima unidade.
        if valor < 1000: #Se o número ainda for menor que 1000, já podemos formatar com a unidade atual ('' ou 'mil').
            return f'{prefixo} {valor: .2f} {unidade}'
        valor /=1000 #Se for maior ou igual a 1000, dividimos por 1000 para converter para a próxima unidade
    return f'{prefixo} {valor: .2f} milhões' #Se passou por todas as unidades do 'for', então o número é milhões.

st.title('DASHBOARD DE VENDAS 🛒')

url = 'https://labdados.com/produtos' #acessar os dados da API.
response = requests.get(url, verify=False) #requisão à API.
dados = pd.DataFrame.from_dict(response.json()) #transforma a requisição em json e depois em DataFrame.


#Criando colunas para Receita e Quantidade de vendas
coluna1, coluna2 = st.columns(2)
with coluna1:
#Adicionar métricas
    st.metric("Receita", formata_numero(dados['Preço'].sum(), 'R$')) #Receita é a métrica, Preço é o valor da Receita (a coluna preço será somada).
with coluna2:
    st.metric("Quantidade de vendas", formata_numero(dados.shape[0])) #Quantidade de linhas do DataFrame. O "shape" retorna qtde de linhas e colunas.

st.dataframe(dados)


