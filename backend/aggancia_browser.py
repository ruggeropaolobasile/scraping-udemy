#D:\VIDEOCORSI\scraping udemy\backend\aggancia_browser.py
import sys
sys.path.append('D:\\VIDEOCORSI\\scraping udemy\\venv\\Lib\\site-packages')
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
from pynput.mouse import Controller
import logging

# Impostazioni di logging per il debug
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class UdemyScraper:
    def __init__(self, db_file, chrome_debugger_address):
        self.db_file = db_file
        self.driver = self._init_driver(chrome_debugger_address)

    def _init_driver(self, chrome_debugger_address):
        logging.debug("Inizializzazione del driver Chrome...")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", chrome_debugger_address)
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            logging.info("Driver Chrome inizializzato correttamente.")
            return driver
        except Exception as e:
            logging.error(f"Errore nell'inizializzazione del driver: {e}")
            raise

    def seleziona_finestra(self, titolo_finestra):
        logging.debug(f"Elenco delle finestre aperte: {self.driver.window_handles}")
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if titolo_finestra in self.driver.title:
                logging.info(f"Finestra '{titolo_finestra}' selezionata.")
                return
        logging.error(f"Finestra con titolo '{titolo_finestra}' non trovata.")
        raise Exception(f"Finestra con titolo '{titolo_finestra}' non trovata.")

    def esegui_azioni(self):
        try:
            logging.debug("Eseguo azioni sul browser già avviato...")
            self.driver.get("https://www.udemy.com/instructor/marketplace-insights/")

            # Usa WebDriverWait per aspettare che l'elemento che ci interessa sia visibile
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='Argomenti promettenti']"))
            )
            logging.info("Pagina caricata correttamente.")

            # Trova e salva gli argomenti
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
                        logging.info(f"Trovati {len(topics)} argomenti promettenti.")
                        for topic in topics:
                            logging.debug(f"Argomento trovato: {topic}")
                        self.salva_in_sqlite(topics)
                    else:
                        logging.warning("Contenitore degli argomenti non trovato.")
        except Exception as e:
            logging.error(f"Errore nell'esecuzione delle azioni: {e}")
            raise

    def salva_in_sqlite(self, topics):
        try:
            logging.debug("Salvataggio dei dati in SQLite...")
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS corsi_udemy  (id INTEGER PRIMARY KEY AUTOINCREMENT, titolo TEXT)")
            for topic in topics:
                cursor.execute("INSERT INTO corsi_udemy  (titolo) VALUES (?)", (topic,))
            conn.commit()
            logging.info("Dati salvati correttamente nel database SQLite.")
        except sqlite3.Error as err:
            logging.error(f"Errore nel salvataggio su SQLite: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def chiudi_driver(self):
        logging.debug("Chiusura del driver...")
        self.driver.quit()

if __name__ == "__main__":
    db_file = r"D:\VIDEOCORSI\scraping udemy\backend\database.db"


    try:
        scraper = UdemyScraper(db_file, "127.0.0.1:9222")

        scraper.seleziona_finestra("Udemy")  # Sostituisci "Udemy" con il titolo della finestra desiderata
        scraper.esegui_azioni()

    except Exception as e:
        logging.error(f"Errore durante l'esecuzione dello scraper: {e}")
    finally:
        scraper.chiudi_driver()
