import csv
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

with open('dados_grupos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Nome do Grupo', 'Link do Grupo', 'Nome do Líder', 'Nome do Segundo Líder', 'Área', 'Situação', 'Data', 'Campus', 'E-mail', 'Equipe'])

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
            actions.move_to_element(element.find_element(By.XPATH, './/div[@class="itemConsulta"]/div[5]/div')).perform()
            time.sleep(3)
            WebDriverWait(driver, 20000).until(EC.element_to_be_clickable(nome_grupo_element)).click()
            driver.switch_to.window(driver.window_handles[1])
            link_grupo = driver.current_url
            situacao = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[1]/div').text
            data = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[4]/div').text
            try:
                campus = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[1]/div/fieldset/div[8]/div').text
            except:
                campus = ''
            try:
                email = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/form/div/div[4]/span[2]/div/fieldset/div[13]/div/a').text
            except:
                email = ''
            equipe_xpath = '//*[@id="indicadores"]'
            equipe =  driver.find_element(By.XPATH, equipe_xpath).get_attribute("outerHTML")
            driver.close()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[0])

            csv_writer.writerow(
                [nome_grupo, link_grupo, nome_lider, nome_segundo_lider, area, situacao, data, campus, email, equipe])
            print(nome_grupo)
        finally:
            print("#")

# Fechando o navegador
# driver.quit()