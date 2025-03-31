import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pynput.mouse import Button, Controller  # Per il click reale con il mouse

class UdemyScraper:
    def __init__(self, db_config, chrome_debugger_address):
        self.db_config = db_config
        self.driver = self._init_driver(chrome_debugger_address)

    def _init_driver(self, chrome_debugger_address):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", chrome_debugger_address)
        return webdriver.Chrome(options=options)

    def seleziona_finestra(self, titolo_finestra):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if titolo_finestra in self.driver.title:
                print(f"Finestra '{titolo_finestra}' selezionata.")
                return
        raise Exception(f"Finestra con titolo '{titolo_finestra}' non trovata.")

    def esegui_azioni(self):
        print("Eseguo azioni sul browser già avviato...")
        self.driver.get("https://www.udemy.com/instructor/marketplace-insights/")
        time.sleep(3)  # Aspetta il caricamento

        target_text = "Argomenti promettenti"
        all_elements = self.driver.find_elements(By.XPATH, "//*")
        promising_topics_header = None

        for element in all_elements:
            if element.text.strip() == target_text:
                promising_topics_header = element
                break

        if promising_topics_header:
            parent = promising_topics_header.find_element(By.XPATH, "..")
            if parent:
                promising_topics_container = promising_topics_header.find_element(By.XPATH, "following-sibling::*[1]")
                if promising_topics_container:
                    topics = [a.text.strip() for a in promising_topics_container.find_elements(By.TAG_NAME, "a")]
                    topics = [topic.replace("Chart", "").replace("End of interactive chart.", "").strip() for topic in topics]
                    for topic in topics:
                        print(topic)
                    self.salva_in_mysql(topics)

    def salva_in_mysql(self, topics):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS argomenti (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255))")
            for topic in topics:
                cursor.execute("INSERT INTO argomenti (nome) VALUES (%s)", (topic,))
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
        'database': 'udemy'
    }

    scraper = UdemyScraper(db_config, "127.0.0.1:9222")

    try:
        scraper.seleziona_finestra("Udemy")  # Sostituisci "Udemy" con il titolo della finestra desiderata
        scraper.esegui_azioni()
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        input("Premi Invio per chiudere il browser...")
        scraper.chiudi_driver()