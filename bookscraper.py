import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base do site
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Dicionário para armazenar os dados
livros = {"Livros": [], "Preços": []}

# Loop para percorrer as páginas
for pagina in range(1, 51):  # De 1 a 50
    # Gerar a URL da página atual
    url = base_url.format(pagina)
    
    # Fazer a requisição HTTP
    res = requests.get(url)
    
    # Verificar se a página existe
    if res.status_code != 200:
        print(f"Não foi possível acessar a página {pagina}.")
        continue

    # Processar o HTML com BeautifulSoup
    extracao = BeautifulSoup(res.text, features="html.parser")

    # Encontrar títulos dos livros e preços
    titulos = extracao.find_all("h3")
    precos = extracao.find_all("p", class_="price_color")

    # Adicionar dados ao dicionário
    for titulo, preco in zip(titulos, precos):
        livros["Livros"].append(titulo.a["title"])  # O título está no atributo 'title'
        livros["Preços"].append(preco.text)  # Preço como texto
    
    print(f"Dados extraídos da página {pagina}.")

# Exibir o resultado
print("Extração completa!")

# Opcional: Salvar em um DataFrame e exportar para CSV
df = pd.DataFrame(livros)
df.to_csv("livros.csv", index=False)
print("Dados salvos em 'livros.csv'")