import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector

class DicolabScraper:
    def __init__(self, db_config, chrome_driver_path):
        self.db_config = db_config
        self.driver = self._init_driver(chrome_driver_path)

    def _init_driver(self, chrome_driver_path):
        options = Options()
        options.add_argument("--headless")  # Esegui Chrome in modalità headless
        service = Service(chrome_driver_path)
        return webdriver.Chrome(service=service, options=options)

    def esegui_azioni(self):
        print("Eseguo azioni sul browser...")
        self.driver.get("https://dicolab.it/corsi/")
        time.sleep(3)  # Aspetta il caricamento

        # Trova gli elementi dei corsi
        corsi_elements = self.driver.find_elements(By.CSS_SELECTOR, ".course-title")
        corsi = [corso.text.strip() for corso in corsi_elements]
        
        # Rimuovi eventuali testi indesiderati
        corsi = [corso for corso in corsi if corso]

        # Stampa i risultati
        for corso in corsi:
            print(corso)
        
        # Salva i risultati in MySQL
        self.salva_in_mysql(corsi)

    def salva_in_mysql(self, corsi):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS corsi (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255))")
            for corso in corsi:
                cursor.execute("INSERT INTO corsi (nome) VALUES (%s)", (corso,))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def chiudi_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'dicolab'
    }
    chrome_driver_path = "C:/chromedriver/chromedriver.exe"  # Sostituisci con il percorso del tuo ChromeDriver

    scraper = DicolabScraper(db_config, chrome_driver_path)

    try:
        scraper.esegui_azioni()
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        scraper.chiudi_driver()