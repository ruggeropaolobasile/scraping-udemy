from sqlalchemy import Column, Integer, String
from db import Base

class Argomento(Base):
    __tablename__ = "argomenti"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True)

    domanda_studenti = Column(String(50))
    percentuale_domanda_studenti = Column(Integer)
    numero_corsi = Column(String(50))
    percentuale_numero_corsi = Column(Integer)
    ricavo_medio = Column(String(50))
    ricavo_massimo = Column(String(50))