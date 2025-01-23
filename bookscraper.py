import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base do site
# A URL possui um padrão onde o número da página será inserido dinamicamente
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Dicionário para armazenar os dados extraídos (títulos e preços dos livros)
livros = {"Livros": [], "Preços": []}

# Loop para percorrer as 50 páginas do site
for pagina in range(1, 51):  # De 1 a 50
    # Gerar a URL da página atual substituindo {} pelo número da página
    url = base_url.format(pagina)
    
    # Fazer a requisição HTTP para obter o conteúdo da página
    res = requests.get(url)
    
    # Verificar se a página existe (status code 200 indica sucesso)
    if res.status_code != 200:
        print(f"Não foi possível acessar a página {pagina}.")
        continue  # Pula para a próxima página se houver erro

    # Processar o HTML retornado com BeautifulSoup para facilitar a extração de dados
    extracao = BeautifulSoup(res.text, features="html.parser")

    # Encontrar todos os títulos dos livros (tag <h3>) e os preços (tag <p> com classe "price_color")
    titulos = extracao.find_all("h3")
    precos = extracao.find_all("p", class_="price_color")

    # Adicionar os dados extraídos ao dicionário 'livros'
    for titulo, preco in zip(titulos, precos):
        # Adiciona o título do livro (presente no atributo 'title' da tag <a>)
        livros["Livros"].append(titulo.a["title"])
        # Adiciona o preço do livro como texto
        livros["Preços"].append(preco.text)
    
    # Exibe uma mensagem indicando que a página foi processada
    print(f"Dados extraídos da página {pagina}.")

# Exibe uma mensagem indicando que a extração foi concluída
print("Extração completa!")

df = pd.DataFrame(livros)  # Converte o dicionário em um DataFrame
df.to_csv("livros.csv", index=False)  # Salva o DataFrame em um arquivo CSV
print("Dados salvos em 'livros.csv'")