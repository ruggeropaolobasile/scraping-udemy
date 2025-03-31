import subprocess

# Funzione di test per eseguire lo script tramite subprocess
def test_scraper():
    # Comando per eseguire il tuo scraper Python (modifica il percorso per adattarlo al tuo sistema)
    command = ["python", "D:/VIDEOCORSI/scraping udemy/backend/aggancia_browser.py"]  # Adatta questo percorso al tuo script

    try:
        # Esegui lo script di scraping come sottoprocesso
        result = subprocess.run(command, capture_output=True, text=True)

        # Controlla se il processo è stato completato senza errori
        if result.returncode == 0:
            print("Script eseguito correttamente.")
            print("Output:", result.stdout)
        else:
            print("Errore durante l'esecuzione dello script.")
            print("Errore:", result.stderr)
    except Exception as e:
        print(f"Errore nell'esecuzione del subprocess: {e}")

# Avvia il test
if __name__ == "__main__":
    test_scraper()
