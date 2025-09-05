import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from login_kommo import login_kommo
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

#Carregando as variaveis de ambiente
load_dotenv()
url_kommo = os.getenv("KOMMO_URL_RELATORIOS_DIA")
kommo_user = os.getenv("KOMMO_USERNAME")
kommo_password = os.getenv("KOMMO_PASSWORD")


def gerar_relatorios_cliente_dia():
#definindo as configurações do chrome
    chrome_options = Options()
    chrome_options.add_argument("--icognito")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")


#Iniciando os drives do navegador
    driver = webdriver.Chrome(options=chrome_options)

    #Entrando no site da kommo para obter o relátorio de clientes diários
    driver.get(url_kommo)
    driver. maximize_window()

    login_kommo(kommo_user, kommo_password, driver)
    
    btn_leads = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[6]/div/div/div[2]/a")))
    btn_leads.click()
    
    element = driver.find_element("tag name", "body")
    ActionChains(driver).move_to_element(element).perform()
    
    time.sleep(1)
    # btn_leads_dropdown = driver.find_element(by=By.CSS_SELECTOR, value="div.list-top-nav__icon-button_dark:nth-child(2)")
    btn_leads_dropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.list-top-nav__icon-button_dark:nth-child(2)")))
    btn_leads_dropdown.click()
    time.sleep(1)
    
    # btn_select_funil_vendas = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[10]/div[2]/div/div/ul/li[1]")
    btn_select_funil_vendas = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[10]/div[2]/div/div/ul/li[1]")))
    btn_select_funil_vendas.click()
    time.sleep(4)
    
    time.sleep(500)


gerar_relatorios_cliente_dia()