import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib
import time

clientes = pd.read_csv('clientes.csv')
browser = webdriver.Chrome()
browser.get('https://web.whatsapp.com/')

while len(browser.find_elements(By.ID, 'side')) == 0:
    time.sleep(1)

def formatar_telefone(numero_telefone: str):
    return '55' + numero_telefone.replace('(', '')\
        .replace(')', '').replace('-', '').replace(' ', '')

for id in range(len(clientes)):
    nome, telefone = clientes.iloc[id] # ['Daniel Batista', '5514981226481']
    print(nome, telefone)
    apelido = nome.split(' ')[0] # ['João', 'Vitor'] => 'João'
    mensagem = f'Olá {apelido}, você recebeu um cupom de 20% de desconto na Pizzaria ABC!'
    mensagem = urllib.parse.quote(mensagem)

    url = f'https://web.whatsapp.com/send/?phone={formatar_telefone(telefone)}&text={mensagem}&type=phone_number&app_absent=0'
    browser.get(url)
    while len(browser.find_elements(By.CSS_SELECTOR,\
        'button[aria-label="Enviar"]')) == 0:
        time.sleep(1)

    browser.find_elements(By.CSS_SELECTOR, 'div[role="textbox"]')[-1]\
    .send_keys(Keys.ENTER)
    time.sleep(10)