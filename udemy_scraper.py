import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from pynput.mouse import Button, Controller  # Per il click reale con il mouse

# Caricare le credenziali dal file .env
load_dotenv()
UDEMY_EMAIL = os.getenv("UDEMY_EMAIL")
UDEMY_PASSWORD = os.getenv("UDEMY_PASSWORD")

# Configurazione WebDriver per collegarsi al browser remoto
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)

def seleziona_finestra(titolo_finestra):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if titolo_finestra in driver.title:
            print(f"Finestra '{titolo_finestra}' selezionata.")
            return
    raise Exception(f"Finestra con titolo '{titolo_finestra}' non trovata.")

def apri_pagina_login():
    print("Apertura della pagina di login di Udemy...")
    driver.get("https://www.udemy.com/join/login-popup/")
    time.sleep(3)  # Aspetta il caricamento

def chiudi_popup_cookie():
    try:
        cookie_button = driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]")
        cookie_button.click()
        print("Popup dei cookie chiuso.")
    except:
        print("Nessun popup dei cookie trovato.")

def inserisci_email():
    print("Inserimento dell'email...")
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(UDEMY_EMAIL)

def clicca_con_mouse_reale(continue_button):
    print("\n🔍 **Tentativo avanzato:** Uso `pynput` per simulare il click reale...")

    # Recupera la posizione esatta del pulsante
    pos = continue_button.location
    size = continue_button.size
    x = pos['x'] + size['width'] / 2
    y = pos['y'] + size['height'] / 2

    # Muove il mouse e clicca
    mouse = Controller()
    mouse.position = (x, y)
    time.sleep(1)
    mouse.click(Button.left, 1)

    print("✅ Click reale simulato con successo! 🎯")

def invia_tab_e_enter(element):
    print("\n🔍 **Tentativo avanzato:** Uso `TAB` + `ENTER` per simulare interazione reale...")

    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    actions.send_keys(Keys.TAB).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ENTER).perform()

    print("✅ Azione completata con `TAB` e `ENTER`. 🎯")

def verifica_elemento_password():
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        print("Elemento della password trovato.")
    except:
        raise Exception("Impossibile trovare l'elemento della password dopo aver cliccato 'Continua con l'email'.")

def inserisci_password():
    print("Inserimento della password...")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    password_input.send_keys(UDEMY_PASSWORD)
    login_button.click()
    time.sleep(5)  # Aspetta il login

def esegui_con_riprova(funzione):
    while True:
        try:
            funzione()
            break
        except Exception as e:
            print(f"Errore: {e}")
            riprova = input("Vuoi riprovare? (s/n): ")
            if riprova.lower() != 's':
                raise

# **Esecuzione dello script**
try:
    seleziona_finestra("Udemy")  # Sostituisci "Udemy" con il titolo della finestra desiderata
    apri_pagina_login()
    chiudi_popup_cookie()
    inserisci_email()
    # clicca_continua_con_email()  # Assicurati di avere questa funzione definita
    esegui_con_riprova(verifica_elemento_password)
    esegui_con_riprova(inserisci_password)
except Exception as e:
    print(f"Errore: {e}")
    input("Premi Invio per chiudere il browser...")

# driver.quit()  # Non lo chiudo per debug