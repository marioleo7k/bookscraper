# Importação das bibliotecas necessárias
import pandas as pd  # Biblioteca para manipulação de dados (DataFrame)
import streamlit as st  # Biblioteca para criar a aplicação web
import plotly.express as px  # Biblioteca para criação de gráficos interativos

# Definir o tema da aplicação (pode ser feito no arquivo config.toml também)
st.set_page_config(page_title="Dashboard de Livros", layout="wide")  # Configura o título da página e o layout da aplicação

# Centralizar o conteúdo da dashboard usando CSS customizado
st.markdown(
    """
    <style>
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        max-width: 100%;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)  # Aplica o CSS no HTML gerado pela aplicação

# Título da Dashboard
st.title("📚 Dashboard de Livros - BookScraper")  # Exibe o título principal da dashboard

# Função para carregar o arquivo CSV
def carregar_dados():
    try:
        # Carrega o arquivo CSV e garante que a codificação está correta
        df = pd.read_csv("livros.csv", encoding="utf-8")
        
        # Limpa caracteres indesejados na coluna 'Preços' (ex: símbolos) e converte para float
        df["Preços"] = df["Preços"].str.replace("[^\\d\\.]", "", regex=True).astype(float)
        return df
    except FileNotFoundError:
        # Caso o arquivo CSV não seja encontrado, exibe um erro
        st.error("Arquivo 'livros.csv' não encontrado. Certifique-se de que o arquivo foi gerado pelo BookScraper.")
        return None
    except Exception as e:
        # Exibe um erro genérico em caso de falha ao carregar os dados
        st.error(f"Erro ao processar os dados: {e}")
        return None

# Carregar os dados a partir do arquivo CSV
df = carregar_dados()

if df is not None:
    # Exibir a tabela de dados carregados
    st.subheader("📋 Dados Extraídos")  # Subtítulo para a seção de dados
    st.dataframe(df)  # Exibe o DataFrame como uma tabela interativa na dashboard

    # Exibe a análise descritiva dos dados
    st.subheader("📊 Análise Descritiva")  # Subtítulo para a seção de análise
    st.write("**Quantidade total de livros:**", len(df))  # Exibe o número total de livros
    st.write("**Preço médio dos livros (£):**", round(df["Preços"].mean(), 2))  # Exibe o preço médio
    st.write("**Preço máximo (£):**", df["Preços"].max())  # Exibe o preço máximo
    st.write("**Preço mínimo (£):**", df["Preços"].min())  # Exibe o preço mínimo

    # Gráfico: Distribuição de Preços
    st.subheader("📉 Distribuição de Preços")  # Subtítulo para o gráfico de distribuição
    fig_hist = px.histogram(
        df, x="Preços", nbins=20, title="Distribuição de Preços dos Livros",  # Cria o histograma
        labels={"Preços": "Preço (£)"}, color_discrete_sequence=['#FF6347']  # Personaliza rótulos e cor
    )
    st.plotly_chart(fig_hist)  # Exibe o gráfico de histograma na dashboard

    # Gráfico: Top 10 Livros Mais Caros
    st.subheader("💸 Top 10 Livros Mais Caros")  # Subtítulo para o gráfico de livros mais caros
    df_top10 = df.nlargest(10, "Preços")  # Filtra os 10 livros mais caros com base na coluna 'Preços'
    fig_bar = px.bar(
        df_top10, x="Livros", y="Preços", title="Top 10 Livros Mais Caros",  # Cria o gráfico de barras
        labels={"Livros": "Título do Livro", "Preços": "Preço (£)"}, color="Preços",  # Personaliza rótulos e cores
        color_continuous_scale="viridis"  # Escolhe a paleta de cores para o gráfico
    )
    
    # Limitação do eixo Y entre 59 e 60
    fig_bar.update_layout(
        xaxis_title="Título do Livro",  # Título do eixo X
        yaxis_title="Preço (£)",  # Título do eixo Y
        yaxis=dict(range=[59, 60]),  # Define os limites do eixo Y para uma faixa específica
        plot_bgcolor="rgba(0,0,0,0)",  # Deixa o fundo transparente
        showlegend=False  # Remove a legenda do gráfico
    )
    st.plotly_chart(fig_bar)  # Exibe o gráfico de barras na dashboard

    # Gráfico: Preço dos Livros por Ordem de Extração
    st.subheader("🔢 Preço dos Livros por Ordem de Extração")  # Subtítulo para o gráfico de preços por ordem
    fig_scatter = px.scatter(
        df, x=range(1, len(df) + 1), y="Preços", title="Preço dos Livros por Ordem",  # Cria o gráfico de dispersão
        labels={"x": "Ordem de Extração", "Preços": "Preço (£)"}, color="Preços",  # Personaliza rótulos e cores
        color_continuous_scale="blues"  # Escolhe a paleta de cores para o gráfico
    )
    st.plotly_chart(fig_scatter)  # Exibe o gráfico de dispersão na dashboard

else:
    # Mensagem de aviso caso o arquivo CSV ainda não esteja disponível
    st.warning("Aguarde o arquivo 'livros.csv' ser gerado pelo BookScraper para visualizar a dashboard.")  # Exibe um aviso