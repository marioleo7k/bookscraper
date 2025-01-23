import pandas as pd
import streamlit as st
import plotly.express as px

# Título da Dashboard
# Define o título que será exibido no topo da dashboard
st.title("Dashboard de Livros - BookScraper")

# Função para carregar o arquivo CSV
def carregar_dados():
    try:
        # Carrega o arquivo CSV e garante que a codificação está correta
        df = pd.read_csv("livros.csv", encoding="utf-8")
        
        # Limpa caracteres indesejados na coluna 'Preços' (ex: símbolos) e converte para float
        df["Preços"] = df["Preços"].str.replace("[^\\d\\.]", "", regex=True).astype(float)
        return df
    except FileNotFoundError:
        # Mostra um erro caso o arquivo CSV não seja encontrado
        st.error("Arquivo 'livros.csv' não encontrado. Certifique-se de que o arquivo foi gerado pelo BookScraper.")
        return None
    except Exception as e:
        # Mostra uma mensagem de erro genérica em caso de falha
        st.error(f"Erro ao processar os dados: {e}")
        return None

# Carregar os dados a partir do arquivo CSV
df = carregar_dados()

if df is not None:
    # Exibir tabela de dados
    # Mostra os dados extraídos em formato de tabela interativa
    st.subheader("Dados Extraídos")
    st.dataframe(df)

    # Análise descritiva
    # Exibe informações estatísticas sobre os dados extraídos
    st.subheader("Análise Descritiva")
    st.write("**Quantidade total de livros:**", len(df))
    st.write("**Preço médio dos livros (£):**", round(df["Preços"].mean(), 2))
    st.write("**Preço máximo (£):**", df["Preços"].max())
    st.write("**Preço mínimo (£):**", df["Preços"].min())

    # Gráfico: Distribuição de Preços
    # Cria um histograma para visualizar a distribuição dos preços
    st.subheader("Distribuição de Preços")
    fig_hist = px.histogram(
        df, x="Preços", nbins=20, title="Distribuição de Preços dos Livros",
        labels={"Preços": "Preço (£)"}, color_discrete_sequence=['blue']
    )
    st.plotly_chart(fig_hist)

    # Gráfico: Top 10 Livros Mais Caros
    # Exibe os 10 livros mais caros em um gráfico de barras
    st.subheader("Top 10 Livros Mais Caros")
    df_top10 = df.nlargest(10, "Preços")  # Filtra os 10 livros mais caros
    fig_bar = px.bar(
        df_top10, x="Livros", y="Preços", title="Top 10 Livros Mais Caros",
        labels={"Livros": "Título do Livro", "Preços": "Preço (£)"}, color="Preços",
        color_continuous_scale="viridis"
    )
    fig_bar.update_yaxes(range=[59.0, 60.0])  # Define os limites do eixo Y
    st.plotly_chart(fig_bar)

    # Gráfico: Preço dos Livros por Ordem de Extração
    # Cria um gráfico de dispersão mostrando a variação dos preços conforme a ordem de extração
    st.subheader("Preço dos Livros por Ordem de Extração")
    fig_scatter = px.scatter(
        df, x=range(1, len(df) + 1), y="Preços", title="Preço dos Livros por Ordem",
        labels={"x": "Ordem de Extração", "Preços": "Preço (£)"}, color="Preços",
        color_continuous_scale="blues"
    )
    st.plotly_chart(fig_scatter)
else:
    # Mensagem de aviso caso o arquivo CSV ainda não esteja disponível
    st.warning("Aguarde o arquivo 'livros.csv' ser gerado pelo BookScraper para visualizar a dashboard.")
