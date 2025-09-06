import os
import time
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
    
    # btn_leads = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.aside__list-item:nth-child(2) > a:nth-child(1)")))
    btn_leads = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[6]/div/div/div[2]/a")))
    btn_leads.click()
    
    element = driver.find_element("tag name", "body")
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(3)
    
    # btn_leads_dropdown = driver.find_element(by=By.CSS_SELECTOR, value="div.list-top-nav__icon-button_dark:nth-child(2)")
    btn_leads_dropdown = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.list-top-nav__icon-button_dark:nth-child(2)")))
    btn_leads_dropdown.click()
    time.sleep(3)
    
    # btn_select_funil_vendas = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[10]/div[2]/div/div/ul/li[1]")
    btn_select_funil_vendas = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[10]/div[2]/div/div/ul/li[1]")))
    btn_select_funil_vendas.click()
    time.sleep(3)
    
    # filter_box = driver.find_element(by=By.ID, value="search_input")
    filter_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search_input")))
    filter_box.click()
    
    conversas = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[2]/h3")))
    driver.execute_script("arguments[0].scrollIntoView(true);", conversas)
    conversas.click()    
    
    data_conversa = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[2]/div/div[5]/div")))
    data_conversa.click()
    
    conversas_dia_anterior = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[2]/div/div[5]/div/div/div[2]/div/ul/li[3]")))
    conversas_dia_anterior.click()
    
    # apply_filters = driver.find_element(by=By.ID, value="filter_apply")
    apply_filters = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "filter_apply")))
    apply_filters.click()
    
    filter_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "search_input")))
    filter_box.click()
    
    select_phases = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[1]/div/div[3]/div/div/div[2]")))
    select_phases.click()
    
    phase_1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[1]/div/div[3]/div/div/div[1]/div/div[7]/label")))
    phase_1.click()
    phase_2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[4]/div[3]/div[1]/div/div[2]/form/div[1]/div[1]/div/div[3]/div/div/div[1]/div/div[8]/label/div[2]")))
    phase_2.click()
    
    apply_filters = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "filter_apply")))
    apply_filters.click()
    
    time.sleep(5)
    
    more_options = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[2]/div/div")))
    more_options.click()
    
    export_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div[1]/div/div/div/div[1]/div[2]/div/div/ul/li[7]/div")))
    export_btn.click()
    time.sleep(3) 
        
    dropdown_filters = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label.modal-export__format:nth-child(2) > div:nth-child(2) > div:nth-child(3) > button:nth-child(2)")))
    dropdown_filters.click()
    
    dropdown_filters_aplicado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label.modal-export__format:nth-child(2) > div:nth-child(2) > div:nth-child(3) > ul:nth-child(1) > li:nth-child(2) > span:nth-child(1)")))
    dropdown_filters_aplicado.click()
    
    export_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.button-input_blue:nth-child(2)")))
    export_btn.click()
    time.sleep(10)
    
    try:
        download_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[13]/div[1]/div/div/div[2]/a/button")))
        download_btn.click()
    except TimeoutException:
        print("Nenhum poupup encontrado")
    
    time.sleep(15)
    driver.quit()


gerar_relatorios_cliente_dia()