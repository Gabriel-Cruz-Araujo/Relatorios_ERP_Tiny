import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from src.utils.login_kommo import login_kommo
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
user = os.getenv("KOMMO_USERNAME")
password = os.getenv("KOMMO_PASSWORD")

chrome_options = Options()
chrome_options.add_argument("--icognito")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")

def vendas_ganhas():
    """
    Rélatorios para gerar relatório de vendas ganhas e
    colocar todos os clientes que estão como vendas ganhas
    em cliente final.
    
    """
    
    url_vendas_ganhas = os.getenv("KOMMO_URL_RELATORIOS_VENDAS_GANHA")
        
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_vendas_ganhas)
    driver.maximize_window()
    
    login_kommo(user, password, driver)
    
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
        download_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div[1]/div/div/div[2]/a")))
        download_btn.click()
    except TimeoutException:
        print("Nenhum poupup encontrado")
    
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    
    while True:
        try:
            time.sleep(5)
            first_lead = driver.find_element(By.XPATH, "(//a[@class='js-navigate-link list-row__template-name__table-wrapper__name-link'])[1]")
            first_lead.click()
            time.sleep(2)
            
            qualify_lead = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[1]/div[1]/form/div/div[1]/div[3]/div/div/div[1]/div/div/div/div[1]")
            qualify_lead.click()
            time.sleep(3)
            
            base_leads = driver.find_element(By.XPATH, value="/html/body/div[11]/div[1]/div/div[2]")
            base_leads.click()
                
            send_to_hopper = driver.find_element(by=By.CSS_SELECTOR, value="/html/body/div[11]/div[1]/div/div[2]/ul/li[8]")
            send_to_hopper.click()
            time.sleep(3)
                
            
            save_changes = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div[1]/div[2]/div[1]/div[2]/button[1]/span/span")    
            save_changes.click()
            time.sleep(4)
                
            back_to_qualify = driver.find_element(by=By.CSS_SELECTOR, value=".js-back-button")
            back_to_qualify.click()
            
            
            
        except NoSuchElementException:
            print("Não há mais leads disponíveis ou a lista de leads está vazia.")
            break
    
    
if __name__ == "__main__":

    vendas_ganhas()