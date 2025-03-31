# main.py - pulito e semplificato con routers e crud
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import corsi, scraping

app = FastAPI()

# CORS per il frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi i router
app.include_router(corsi.router)
app.include_router(scraping.router)

@app.get("/")
def read_root():
    return {"message": "API attiva con MySQL!"}

# Avvia il server con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

