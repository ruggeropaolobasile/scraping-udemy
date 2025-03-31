# routers/scraping.py

from fastapi import APIRouter
from subprocess import Popen, PIPE

router = APIRouter()

@router.get("/api/scraper")
def run_scraper():
    try:
        process = Popen(['python', 'D:/VIDEOCORSI/scraping udemy/backend/aggancia_browser.py'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return {"error": stderr.decode()}
        return {"message": "Scraping completato", "output": stdout.decode()}
    except Exception as e:
        return {"error": str(e)}

@router.get("/api/arricchisci/{titolo}")
def arricchisci_corso(titolo: str):
    try:
        print(f"Ricevuto il titolo: {titolo}")
        process = Popen(['python', 'D:/VIDEOCORSI/scraping udemy/backend/arricchisci.py', titolo], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return {"error": stderr.decode()}
        return {"message": "Arricchimento completato", "output": stdout.decode()}
    except Exception as e:
        return {"error": str(e)}
