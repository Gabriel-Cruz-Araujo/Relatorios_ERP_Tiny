import os
import time
import pyautogui
from selenium import webdriver
from dotenv import load_dotenv
from src.utils.login_kommo import login_kommo
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

#Carregando as variaveis de ambiente
load_dotenv()
url_kommo = os.getenv("KOMMO_URL_CONVERSAS_DIA")
kommo_user = os.getenv("KOMMO_USERNAME")
kommo_password = os.getenv("KOMMO_PASSWORD")

download_dir = ("C:/Users/equip/Documents/relatorios/contatos_diarios")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    
    
def gerar_relatorios_cliente_dia():
    """
    Código para gerar o relátorio dos clientes
    contactados no dia.
    
    """
    
    #definindo as configurações do chrome
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")

    
#Iniciando os drives do navegador
    driver = webdriver.Chrome(options=chrome_options)

    #Entrando no site da kommo para obter o relátorio de clientes diários
    driver.get(url_kommo)
    driver. maximize_window()

    login_kommo(kommo_user, kommo_password, driver)
    
    time.sleep(5)
    
    more_options_btn = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[2]/div/div/button/span")
    more_options_btn.click()
    time.sleep(3)
    
    export_btn = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[2]/div/div/ul/li[7]/div/span[2]")
    export_btn.click()
    time.sleep(3)
        
    dropdown_filters = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label.modal-export__format:nth-child(2) > div:nth-child(2) > div:nth-child(3) > button:nth-child(2)")))
    dropdown_filters.click()
    
    time.sleep(3) 
    dropdown_filters_aplicado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label.modal-export__format:nth-child(2) > div:nth-child(2) > div:nth-child(3) > ul:nth-child(1) > li:nth-child(2)")))
    dropdown_filters_aplicado.click()
    
    time.sleep(3) 
    export_excell_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.button-input_blue:nth-child(2)")))
    export_excell_btn.click()
    time.sleep(10)

    download_btn = driver.find_element(by=By.CSS_SELECTOR, value=".modal-export__save-button")
    download_btn.click()
    time.sleep(5)
    
    pyautogui.press("enter")
    
    time.sleep(5)
    driver.quit()
    
if __name__ == "__main__":
    gerar_relatorios_cliente_dia()