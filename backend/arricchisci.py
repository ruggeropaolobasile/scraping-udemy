import sys
import time
import requests
from scraper_logger import log_scraper, log_warning, log_error, log_section
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class UdemyScraper:
    def __init__(self, db_file, chrome_debugger_address):
        self.db_file = db_file
        self.driver = self._init_driver(chrome_debugger_address)

    def _init_driver(self, chrome_debugger_address):
        log_scraper("Inizializzazione del driver Chrome...")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", chrome_debugger_address)
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            log_scraper("Driver Chrome inizializzato correttamente.")
            return driver
        except Exception as e:
            log_error(f"Errore nell'inizializzazione del driver: {e}")
            raise

    def arricchisci_topic(self, topic):
        log_scraper(f"Chiamato arricchisci_topic con il parametro: {topic}")
        log_scraper("Navigando verso l'URL di Udemy...")
        try:
            log_scraper(f"Arricchendo i dati per l'argomento: {topic}")
            self.driver.get("https://www.udemy.com/instructor/marketplace-insights/?q=&lang=en")

            # Attendere che la casella di ricerca sia visibile
            # Usiamo contains per essere più flessibili, anche se cambia "ad es."
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'fotografia, fotografia di viaggio, JavaScript')]"))
            )

            search_box.clear()
            search_box.send_keys(topic)  # Inserisci il nome del topic
            search_box.send_keys(Keys.RETURN)  # Simula la pressione del tasto "Enter"

            log_scraper(f"Topic '{topic}' inserito e ricerca avviata.")

            # Attendere un po' di tempo per essere sicuri che la pagina si sia caricata completamente.
            time.sleep(4)



            log_scraper(f"Risultati per '{topic}' caricati con successo.")

            results = {}
            
            metrics_to_extract = {
                "Domanda degli studenti": "student_demand",
                "Numero di corsi": "number_of_courses",
                "Ricavo medio mensile": "average_monthly_revenue",
                "Ricavo massimo mensile": "maximum_monthly_revenue",
            }

            for metric_title_it, metric_key in metrics_to_extract.items():
                try:
                    metric_title_element = self.driver.find_element(
                        By.XPATH,
                        f"//div[contains(@class, 'course-label-metrics--metrics-title--27PPb') and contains(text(), '{metric_title_it}')]",
                    )
                    parent = metric_title_element.find_element(By.XPATH, "..")
                    sibling = parent.find_element(By.XPATH, "following-sibling::*")
                    metric_value = sibling.text.strip()
                    results[metric_key] = metric_value
                    log_scraper(f"{metric_title_it} per '{topic}': {metric_value}")

                    #  ✅ Prova a leggere anche il valore percentuale
                    #  ✅ Specificamente extract student demand percentage using the confirmed selector
                    # Extract Student Demand Percentage
                    try:
                        slider_value_element = self.driver.find_element(By.CSS_SELECTOR, ".slider--slider--rIcaE:not(.slider--slider-decreasing--BS8hT) .slider--slider-value--JL8Sq")
                        left_style = slider_value_element.get_attribute("style")
                        percentage_str = left_style.split(": ")[1].rstrip(";")
                        percentage = round(float(percentage_str.rstrip("%")))  #  <---  The fix: use float() and round()
                        results["student_demand_percentage"] = percentage
                        log_scraper(f"Student Demand Percentage for '{topic}': {percentage}%")
                    except Exception as e:
                        log_error(f"Error retrieving Student Demand Percentage for '{topic}': {e}")
                        results["student_demand_percentage"] = "Error"


                    # Extract Number of Courses Percentage
                    try:
                        slider_corsi_element = self.driver.find_element(By.CSS_SELECTOR, ".slider--slider--rIcaE.slider--slider-decreasing--BS8hT .slider--slider-value--JL8Sq")
                        left_style = slider_corsi_element.get_attribute("style")
                        percentage_str = left_style.split(": ")[1].rstrip(";")
                        percentage = round(float(percentage_str.rstrip("%")))
                        results["number_of_courses_percentage"] = percentage
                        log_scraper(f"Number of Courses Percentage for '{topic}': {percentage}%")
                    except Exception as e:
                        log_error(f"Error retrieving Number of Courses Percentage for '{topic}': {e}")
                        results["number_of_courses_percentage"] = "Error"

                except Exception as e:
                    log_error(f"Errore nel reperire {metric_title_it} per '{topic}': {e}")
                    results[metric_key] = "Errore"

            
            return {"topic": topic, **results}

        except Exception as e:
            log_error(f"Errore nell'arricchire i dati per '{topic}': {e}")
            return {"topic": topic, "student_demand": "Errore","number_of_courses": "Errore","average_monthly_revenue": "Errore","maximum_monthly_revenue": "Errore"}

    def chiudi_driver(self):
        log_scraper("Chiusura del driver...")
        self.driver.quit()

if __name__ == "__main__":
    # Controlla che un parametro (topic) sia passato
    if len(sys.argv) < 2:
        print("Utilizzo: python arricchisci.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    # Imposta il percorso del database (se necessario per altre operazioni)
    db_file = r"D:\VIDEOCORSI\scraping udemy\backend\database.db"

    try:
        scraper = UdemyScraper(db_file, "127.0.0.1:9222")
        risultato = scraper.arricchisci_topic(topic)
        print(risultato)
    except Exception as e:
        log_error(f"Errore durante l'esecuzione dello scraper: {e}")

    try:
        print(f"Ricevuto il titolo: {risultato}")
        response = requests.post("http://localhost:8000/api/insights", json=risultato)
        if response.status_code == 201:
            print("Dati inseriti correttamente nel backend!")
        else:
            print("Errore nell'inserimento:", response.text)
    except Exception as e:
        print("Eccezione durante la chiamata al backend:", e)


    finally:
        scraper.chiudi_driver()