import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time
import sys

try:
    url_planilha = sys.argv[1]
except:
    url_planilha = 'clientes.csv'

try:
    tipo_planilha = sys.argv[2].lower()
except:
    tipo_planilha = 'csv'

if tipo_planilha == 'csv':
    clientes = pd.read_csv(url_planilha)
elif tipo_planilha == 'xlsx':
    clientes = pd.read_excel(url_planilha)
else:
    print(f'O programa não consegue ler arquivos do tipo {tipo_planilha}')

mensagem = input('Digite sua mensagem (use o texto *nome* para usar o nome do usuario na mensagem): ')

browser = webdriver.Chrome()
browser.get('https://web.whatsapp.com/')

while len(browser.find_elements(By.ID, 'side')) == 0:
    time.sleep(1)

def formatar_telefone(numero_telefone: str):
    return '55' + numero_telefone.replace('(', '')\
        .replace(')', '').replace('-', '').replace(' ', '')

for id in range(len(clientes)):
    nome, telefone = clientes.iloc[id]
    apelido = nome.split(' ')[0]
    mensagem_usuario = mensagem.replace('*nome*', apelido)
    mensagem_usuario = urllib.parse.quote(mensagem_usuario)

    url = f'https://web.whatsapp.com/send/?phone={formatar_telefone(telefone)}&text={mensagem_usuario}&type=phone_number&app_absent=0'
    browser.get(url)
    while len(browser.find_elements(By.CSS_SELECTOR,\
        'button[aria-label="Enviar"]')) == 0:
        time.sleep(1)

    browser.find_elements(By.CSS_SELECTOR, 'div[role="textbox"]')[-1] \
    .send_keys(Keys.ENTER)

    browser.find_elements(By.CSS_SELECTOR, 'input[type="file"]')[0]\
    .send_keys("C:/Users/Biston/IdeaProjects/autowhatsapp/autowhatsapp/imagem.jpg")

    while len(browser.find_elements(By.CSS_SELECTOR, 'div[aria-label="Enviar"]')) == 0:
        time.sleep(1)
    else:
        browser.find_element(By.CSS_SELECTOR, 'div[aria-label="Enviar"]').click()

    time.sleep(10)

