import time
import json
import sqlite3
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
DB_PATH = "D:/VIDEOCORSI/scraping udemy/backend/database.db"
KEYWORD_LOG_FILE = "keyword_log.json"
DEBUGGER_ADDRESS = "127.0.0.1:9222"

# === SETUP DB ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS corsi_udemy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titolo TEXT UNIQUE,
    link TEXT,
    domanda TEXT,
    numero_corsi TEXT,
    ricavo_medio TEXT,
    ricavo_massimo TEXT
)
""")
conn.commit()

# === SELENIUM DRIVER ===
options = webdriver.ChromeOptions()
options.debugger_address = DEBUGGER_ADDRESS
print(f"🔗 Collegamento a Chrome esistente su {DEBUGGER_ADDRESS}...")
driver = webdriver.Chrome(options=options)
driver.get("https://www.udemy.com/instructor/marketplace-insights/")

# === ATTESA CAMPO INPUT ===
wait = WebDriverWait(driver, 10)
input_xpath = "//input[contains(@placeholder, 'fotografia')]"

# === LETTERE DA ESPLORARE ===
alphabet = list("abcdefghijklmnopqrstuvwxyz")

trovate = set()

for lettera in alphabet:
    print(f"\n>>> Cercando suggerimenti per: '{lettera}'")
    try:
        input_element = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        input_element.clear()
        input_element.send_keys(lettera)
        time.sleep(3)

        suggestions = driver.find_elements(By.XPATH, "//button[contains(@class,'ud-btn') and contains(@class,'ud-autosuggest-suggestion')]")
        print(f"  Suggerimenti trovati: {len(suggestions)}")

        for el in suggestions:
            keyword = el.text.strip()
            if keyword and keyword not in trovate:
                trovate.add(keyword)
                print(f"  [+] {keyword}")
                cursor.execute("SELECT COUNT(*) FROM corsi_udemy WHERE titolo = ?", (keyword,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO corsi_udemy (titolo, link, domanda_studenti, numero_corsi, ricavo_medio, ricavo_massimo)
                        VALUES (?, '', NULL, NULL, NULL, NULL)
                    """, (keyword,))
                    conn.commit()
                    print(f"    ✅ Salvato nel DB")
                else:
                    print(f"    ⚠️ Già presente nel DB")
    except Exception as e:
        print(f"Errore durante la lettera '{lettera}': {e}")

# === SALVATAGGIO LOG JSON ===
with open(KEYWORD_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(sorted(list(trovate)), f, indent=2, ensure_ascii=False)

print(f"\n✅ Totale keyword trovate e salvate: {len(trovate)}")
driver.quit()
conn.close()