import requests
import pandas as pd
import time # Importamos a biblioteca time para adicionar pausas entre as requisições

# --- Configuração da Requisição ---
# É uma boa prática não deixar sua chave de API diretamente no código.
# Considere usar variáveis de ambiente para mais segurança.
API_KEY = "14dc2cd32bmsh2de72cf1b6b4717p164ae8jsncdcf51f89a44" 

url = "https://real-time-amazon-data.p.rapidapi.com/products-by-category"

headers = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

# Parâmetros base da busca (a 'page' será atualizada no loop)
querystring = {
    "category_id":"18991136011",
    "country":"BR",
    "sort_by":"RELEVANCE",
    "min_price":"100",
    "max_price":"500",
    "product_condition":"NEW",
    "is_prime":"false",
    "deals_and_discounts":"NONE"
}

# --- Coleta de Dados ---
todos_os_produtos = [] # Lista para armazenar os produtos de todas as páginas

# O range(5, 16) irá gerar números de 5 a 15 (o último número não é incluído)
for numero_pagina in range(8, 30):
    print(f"Buscando dados da página {numero_pagina}...")
    
    # Atualiza o dicionário de parâmetros com a página atual
    querystring['page'] = str(numero_pagina)
    
    # Faz a requisição para a API
    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        # Verifica se a requisição foi bem-sucedida (código 200)
        if response.status_code == 200:
            data = response.json()
            
            # Extrai a lista de produtos da resposta JSON
            # A estrutura da resposta é {'status': 'OK', 'data': {'total_products': ..., 'products': [...]}}
            produtos_da_pagina = data['data']['products']
            
            # Adiciona os produtos encontrados nesta página à nossa lista principal
            if produtos_da_pagina:
                todos_os_produtos.extend(produtos_da_pagina)
                print(f"  -> {len(produtos_da_pagina)} produtos encontrados na página {numero_pagina}.")
            else:
                print(f"  -> Nenhum produto encontrado na página {numero_pagina}. A busca pode ter terminado.")
                break # Se uma página não retorna produtos, podemos parar o loop
                
        else:
            print(f"  -> Erro ao buscar a página {numero_pagina}. Status Code: {response.status_code}")
            print(f"  -> Resposta: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"  -> Ocorreu um erro de conexão: {e}")
        continue # Pula para a próxima página em caso de erro de rede

    # É uma boa prática esperar um pouco entre as requisições para não sobrecarregar a API
    time.sleep(1) 

# --- Salvando os Dados em CSV ---
if todos_os_produtos:
    print("\nConvertendo dados e salvando em CSV...")
    
    # Cria um DataFrame do Pandas com a lista de todos os produtos
    df_produtos = pd.DataFrame(todos_os_produtos)
    
    # Define o nome do arquivo
    nome_arquivo_csv = 'pet_produtos.csv'
    
    # Salva o DataFrame em um arquivo CSV
    # index=False: para não salvar o índice do DataFrame no arquivo
    # encoding='utf-8-sig': para garantir a correta exibição de caracteres especiais (como ç, ã) no Excel
    df_produtos.to_csv(nome_arquivo_csv, index=False, encoding='utf-8-sig')
    
    print(f"Arquivo '{nome_arquivo_csv}' criado com sucesso com {len(df_produtos)} produtos!")
else:
    print("\nNenhum produto foi coletado. O arquivo CSV não foi criado.")