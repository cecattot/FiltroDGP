import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Função para extrair informações do HTML
def extrair_informacoes_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table')

    # Verificar se a tabela foi encontrada
    if tabela is not None:
        # Inicializar listas para armazenar informações
        formacao_academica = []
        pesquisadores = []
        estudantes = []
        tecnicos = []
        colaboradores_estrangeiros = []
        total = []

        # Iterar sobre as linhas da tabela
        for linha in tabela.find_all('tr'):
            colunas = linha.find_all('td')
            if colunas:
                formacao_academica.append(colunas[0].text.strip())
                pesquisadores.append(int(colunas[1].text.strip()))
                estudantes.append(int(colunas[2].text.strip()))
                tecnicos.append(int(colunas[3].text.strip()))
                colaboradores_estrangeiros.append(int(colunas[4].text.strip()))
                total.append(int(colunas[5].text.strip()))

        # Criar um DataFrame para armazenar as informações
        df = pd.DataFrame({
            'Formação acadêmica': formacao_academica,
            'Pesquisadores': pesquisadores,
            'Estudantes': estudantes,
            'Técnicos': tecnicos,
            'Colaboradores estrangeiros': colaboradores_estrangeiros,
            'Total': total
        })

        # Criar a representação resumida
        resumo_df = pd.DataFrame(index=df.index)
        for coluna in ['Pesquisadores', 'Estudantes', 'Técnicos', 'Colaboradores estrangeiros']:
            for i, formacao in enumerate(df['Formação acadêmica']):
                resumo_df[f"{coluna}_{formacao if i < len(df) else 'Não Informado'}"] = df[coluna][i] if i < len(
                    df) else 0

        return resumo_df.to_dict(orient='records')
    else:
        # Retorna uma lista vazia se a tabela não for encontrada
        return []

# Função para extrair informações da tabela de pesquisadores
def extrair_informacoes_pesquisadores(driver, xpath):
    try:
        # Aguardar a tabela estar presente na página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Localizar a tabela de pesquisadores
        tabela = driver.find_element(By.XPATH, xpath)

        # Inicializar lista para armazenar informações
        pesquisadores_info = []

        # Iterar sobre as linhas da tabela de pesquisadores
        for linha in tabela.find_elements(By.XPATH, './/tr[@role="row"]'):
            colunas = linha.find_elements(By.XPATH, './/td[@role="gridcell"]')

            if colunas:
                nome = colunas[0].text.strip()
                titulacao_maxima = colunas[1].text.strip()
                data_inclusao = colunas[2].text.strip()

                # Construir o ID dinamicamente
                id = linha.get_attribute('data-ri')
                actions = ActionChains(driver)
                actions.move_to_element(
                    linha.find_element(By.XPATH, f'.//a[contains(@id, "btnAcessoLattes2")]')).perform()
                time.sleep(15)
                WebDriverWait(driver, 20000).until(EC.element_to_be_clickable(
                    linha.find_element(By.XPATH, f'.//a[contains(@id, "btnAcessoLattes2")]'))).click()
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[2])
                link_lattes = driver.current_url
                driver.close()
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[1])

                pesquisadores_info.append(
                    {'Nome': nome, 'Titulação Máxima': titulacao_maxima, 'Data de Inclusão': data_inclusao,
                     'Link Lattes': link_lattes})
        return pesquisadores_info
    except Exception as e:
        print(f"Erro ao extrair informações de pesquisadores: {str(e)}")
        return []


# Configurando o WebDriver (utilize o caminho adequado para o seu ambiente)
driver = webdriver.Chrome()

# Abrindo a página
url = "http://dgp.cnpq.br/dgp/faces/consulta/consulta_parametrizada.jsf"
driver.get(url)

# Aguardando o elemento ser clicável e clicando no botão
button_xpath = '//*[@id="idFormConsultaParametrizada:buscaRefinada"]/span'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()

# Selecionando opções nos drop-downs
dropdown1_xpath = '/html/body/div[3]/div/div/form[2]/span/fieldset/span[3]/span[1]/div[1]/div/div[1]'
option1_xpath = '/html/body/div[9]/div/ul/li[2]'
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath))).click()
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, option1_xpath))).click()

time.sleep(5)

dropdown2_xpath = '/html/body/div[3]/div/div/form[2]/span/fieldset/span[3]/span[1]/div[2]/div/div[1]'
option2_xpath = '/html/body/div[17]/div/ul/li[4]'
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, dropdown2_xpath))).click()
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, option2_xpath))).click()

time.sleep(5)

dropdown3_xpath = '/html/body/div[3]/div/div/form[2]/span/fieldset/span[3]/span[1]/div[3]/div/div[1]'
option3_xpath = '/html/body/div[17]/div/ul/li[4]'
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, dropdown3_xpath))).click()
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, option3_xpath))).click()

# Clicando no botão final
final_button_xpath = '/html/body/div[3]/div/div/form[2]/span/fieldset/div[5]/button[1]/span[2]'
WebDriverWait(driver, 20000).until(EC.element_to_be_clickable((By.XPATH, final_button_xpath))).click()

# Aguardando 15 segundos
time.sleep(15)

# Acessando o segundo dropdown e selecionando a terceira opção
dropdown_second_xpath = '/html/body/div[3]/div/div/form[2]/span/div[1]/div[2]/select'
option_third_xpath = '/html/body/div[3]/div/div/form[2]/span/div[1]/div[2]/select/option[3]'
WebDriverWait(driver, 90000).until(EC.element_to_be_clickable((By.XPATH, dropdown_second_xpath))).click()
WebDriverWait(driver, 90000).until(EC.element_to_be_clickable((By.XPATH, option_third_xpath))).click()

# Aguardando mais 15 segundos
time.sleep(15)

# Iterando sobre os elementos e salvando em um arquivo CSV
with open('dados_grupos.csv', 'w', newline='', encoding='utf-8') as csvfile, open('pesquisadores.csv', 'w', newline='',
                                                                                  encoding='utf-8') as pesquisadores_csvfile:
    csv_writer = csv.writer(csvfile)
    pesquisadores_csv_writer = csv.writer(pesquisadores_csvfile)

    csv_writer.writerow(
        ['id', 'Nome Grupo', 'Link Grupo', 'Nome Líder', 'Nome Segundo Líder', 'Área', 'Situação', 'Criação',
         'Atualização', 'Campus', 'Email', 'Equipe_Pesquisadores_Doutorado', 'Equipe_Pesquisadores_Mestrado',
         'Equipe_Pesquisadores_Mestrado Profissional', 'Equipe_Pesquisadores_Especialização',
         'Equipe_Pesquisadores_Graduação', 'Equipe_Estudantes_Doutorado', 'Equipe_Estudantes_Mestrado',
         'Equipe_Estudantes_Mestrado Profissional', 'Equipe_Estudantes_Especialização', 'Equipe_Estudantes_Graduação',
         'Equipe_Técnicos_Doutorado', 'Equipe_Técnicos_Mestrado', 'Equipe_Técnicos_Mestrado Profissional',
         'Equipe_Técnicos_Especialização', 'Equipe_Técnicos_Graduação', 'Equipe_Colaboradores estrangeiros_Doutorado',
         'Equipe_Colaboradores estrangeiros_Mestrado', 'Equipe_Colaboradores estrangeiros_Mestrado Profissional',
         'Equipe_Colaboradores estrangeiros_Especialização', 'Equipe_Colaboradores estrangeiros_Graduação'])
    pesquisadores_csv_writer.writerow(
        ['ID do Grupo', 'Nome', 'Tipo', 'Titulação Máxima', 'Data de Inclusão', 'Link Lattes'])

    elements_xpath = '//*[@id="idFormConsultaParametrizada:resultadoDataList_list"]/li'
    elements = driver.find_elements(By.XPATH, elements_xpath)

    for index, element in enumerate(elements):
        try:
            nome_grupo_element = element.find_element(By.XPATH, './/div[@class="controls"]/a')
            nome_grupo = nome_grupo_element.text
            nome_lider = element.find_element(By.XPATH,
                                              './/div[@class="controls"]/a[contains(@id, "idBtnVisualizarEspelhoLider1")]').text

            try:
                nome_segundo_lider = element.find_element(By.XPATH,
                                                          './/div[@class="controls"]/a[contains(@id, "idBtnVisualizarEspelhoLider2")]').text
            except:
                nome_segundo_lider = ''

            area = element.find_element(By.XPATH, './/div[@class="itemConsulta"]/div[5]/div').text

            # Usando ação de rolagem para o elemento
            actions = ActionChains(driver)
            actions.move_to_element(
                element.find_element(By.XPATH, './/div[@class="itemConsulta"]/div[5]/div')).perform()
            time.sleep(30)
            WebDriverWait(driver, 20000).until(EC.element_to_be_clickable(nome_grupo_element)).click()
            driver.switch_to.window(driver.window_handles[1])
            link_grupo = str(driver.current_url)
            id_grupo = re.search(r'(\d+)$', link_grupo).group(1)
            criacao = driver.find_element(By.XPATH,
                                          '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[2]/div').text
            situacao = driver.find_element(By.XPATH,
                                           '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[1]/div').text
            atualizacao = driver.find_element(By.XPATH,
                                              '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[4]/div').text
            try:
                campus = driver.find_element(By.XPATH,
                                             '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[8]/div').text
            except:
                campus = ''
            try:
                email = driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[2]/div/fieldset/div[13]/div/a').text
            except:
                email = ''

            equipe_xpath = '//*[@id="indicadores"]'
            equipe_html = driver.find_element(By.XPATH, equipe_xpath).get_attribute("outerHTML")

            # Processando o campo 'equipe' conforme o segundo código enviado
            equipe_info = extrair_informacoes_html(equipe_html)
            equipe_info = equipe_info[0] if equipe_info else {}

            csv_writer.writerow(
                [id_grupo, nome_grupo, link_grupo, nome_lider, nome_segundo_lider, area,
                 situacao, criacao, atualizacao, campus,
                 email,
                 equipe_info.get('Pesquisadores_Doutorado', 0),
                 equipe_info.get('Pesquisadores_Mestrado', 0),
                 equipe_info.get('Pesquisadores_Mestrado Profissional', 0),
                 equipe_info.get('Pesquisadores_Especialização', 0),
                 equipe_info.get('Pesquisadores_Graduação', 0),
                 equipe_info.get('Estudantes_Doutorado', 0),
                 equipe_info.get('Estudantes_Mestrado', 0),
                 equipe_info.get('Estudantes_Mestrado Profissional', 0),
                 equipe_info.get('Estudantes_Especialização', 0),
                 equipe_info.get('Estudantes_Graduação', 0),
                 equipe_info.get('Técnicos_Doutorado', 0),
                 equipe_info.get('Técnicos_Mestrado', 0),
                 equipe_info.get('Técnicos_Mestrado Profissional', 0),
                 equipe_info.get('Técnicos_Especialização', 0),
                 equipe_info.get('Técnicos_Graduação', 0),
                 equipe_info.get('Colaboradores estrangeiros_Doutorado', 0),
                 equipe_info.get('Colaboradores estrangeiros_Mestrado', 0),
                 equipe_info.get('Colaboradores estrangeiros_Mestrado Profissional', 0),
                 equipe_info.get('Colaboradores estrangeiros_Especialização', 0),
                 equipe_info.get('Colaboradores estrangeiros_Graduação', 0)])

            print(nome_grupo)

            # Processando o campo 'pesquisadores' conforme a nova tabela
            pesquisadores_info = extrair_informacoes_pesquisadores(driver,
                                                                   '//*[@id="idFormVisualizarGrupoPesquisa:j_idt271_data"]')

            # Adicionando informações dos pesquisadores ao CSV
            for pesquisador_info in pesquisadores_info:
                pesquisadores_csv_writer.writerow(
                    [re.search(r'(\d+)$', link_grupo).group(1), 'Pesquisador', pesquisador_info['Nome'],
                     pesquisador_info['Titulação Máxima'], pesquisador_info['Data de Inclusão'],
                     pesquisador_info['Link Lattes']])

            # Processando o campo 'ESTUDANTES' conforme a nova tabela
            estudantes_info = extrair_informacoes_pesquisadores(driver,
                                                                '//*[@id="idFormVisualizarGrupoPesquisa:j_idt288"]')

            # Adicionando informações dos estudantes ao CSV
            for estudantes_info in estudantes_info:
                pesquisadores_csv_writer.writerow(
                    [re.search(r'(\d+)$', link_grupo).group(1), 'Estudante', estudantes_info['Nome'],
                     estudantes_info['Titulação Máxima'], estudantes_info['Data de Inclusão'],
                     estudantes_info['Link Lattes']])

            # Processando o campo 'TAES' conforme a nova tabela
            taes_info = extrair_informacoes_pesquisadores(driver,
                                                          '//*[@id="idFormVisualizarGrupoPesquisa:j_idt305_data"]')

            # Adicionando informações dos TAES ao CSV
            for tae_info in taes_info:
                pesquisadores_csv_writer.writerow(
                    [re.search(r'(\d+)$', link_grupo).group(1), 'TAE', tae_info['Nome'], tae_info['Titulação Máxima'],
                     tae_info['Data de Inclusão'], tae_info['Link Lattes']])

            # Processando o campo 'COLABORADORES ESTRANGEIROS' conforme a nova tabela
            colEstrangeiros_info = extrair_informacoes_pesquisadores(driver,
                                                                     '//*[@id="idFormVisualizarGrupoPesquisa:j_idt322_data"]')

            # Adicionando informações dos Colaboradores Estrangeiros ao CSV
            for colEstrangeiro_info in colEstrangeiros_info:
                pesquisadores_csv_writer.writerow(
                    [re.search(r'(\d+)$', link_grupo).group(1), 'Colaborador Estrangeiro', colEstrangeiro_info['Nome'],
                     colEstrangeiro_info['Titulação Máxima'], colEstrangeiro_info['Data de Inclusão'],
                     colEstrangeiro_info['Link Lattes']])

            driver.close()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])

        finally:
            print("#")

# Fechando o navegador
# driver.quit()