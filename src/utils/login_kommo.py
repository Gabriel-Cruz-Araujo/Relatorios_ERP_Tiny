import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
load_dotenv()

def login_kommo(kommo_user, kommo_password, driver):
    """
    Função para ser reutilizada, a função
    serve para fazer o login automaticamente na 
    kommo e se tiver um poupup fecha-lo.
    
    """
    login_username_kommo = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div[1]/span/input")))
    login_username_kommo.send_keys(kommo_user)
    
    time.sleep(1)

    login_password_kommo = driver.find_element(by=By.ID, value="password")
    login_password_kommo.send_keys(kommo_password)
    
    login_button_kommo = driver.find_element(by=By.CSS_SELECTOR, value="#auth_submit")
    login_button_kommo.click()
    
    try:
        time.sleep(5)
        popup_kommo = driver.find_element(by=By.CSS_SELECTOR, value="body > div.modal.modal-list > div.modal-scroller.custom-scroll > div > div > button")
        popup_kommo.click()
    except TimeoutException:
        print("Nenhum poupup encontrado")