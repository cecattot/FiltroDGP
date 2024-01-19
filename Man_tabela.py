import pandas as pd
from bs4 import BeautifulSoup

# Ler o CSV
df = pd.read_csv('dados_grupos.csv')

# Função para extrair informações do HTML
def extrair_informacoes_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table')

    # Verificar se a tabela foi encontrada
    if tabela is not None:
        # Inicializar dicionário para armazenar informações
        info = {'Formação acadêmica': [], 'Pesquisadores': [], 'Estudantes': [], 'Técnicos': [],
                'Colaboradores estrangeiros': [], 'Total': []}

        # Iterar sobre as linhas da tabela
        for linha in tabela.find_all('tr'):
            colunas = linha.find_all('td')
            if colunas:
                info['Formação acadêmica'].append(colunas[0].text.strip())
                info['Pesquisadores'].append(int(colunas[1].text.strip()))
                info['Estudantes'].append(int(colunas[2].text.strip()))
                info['Técnicos'].append(int(colunas[3].text.strip()))
                info['Colaboradores estrangeiros'].append(int(colunas[4].text.strip()))
                info['Total'].append(int(colunas[5].text.strip()))

        return info
    else:
        # Retorna um dicionário vazio se a tabela não for encontrada
        return {}

# Aplicar a função para extrair informações do HTML
df['Equipe'] = df['Equipe'].apply(extrair_informacoes_html)

# Criar a representação resumida
resumo_df = pd.DataFrame(index=df.index)
for coluna in ['Pesquisadores', 'Estudantes', 'Técnicos', 'Colaboradores estrangeiros']:
    for i, formacao in enumerate(df['Equipe'].apply(lambda x: x.get('Formação acadêmica', []))):
        resumo_df[f"{coluna}_{formacao[i] if i < len(formacao) else 'Não Informado'}"] = df.apply(lambda row: row['Equipe'][coluna][i] if i < len(row['Equipe'][coluna]) else 0, axis=1)

# Adicionar colunas de resumo ao CSV original
df = pd.concat([df, resumo_df], axis=1)

# Salvar o resultado no CSV original
df.to_csv('dados_grupos.csv', index=False)
