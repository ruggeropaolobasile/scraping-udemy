#database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./database.db"  # Usa aiosqlite per SQLite asincrono

# Creiamo l'engine asincrono
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

class CorsoUdemy(Base):
    __tablename__ = "corsi_udemy"

    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, index=True)
    link = Column(String)

    domanda_studenti = Column(String, nullable=True)
    percentuale_domanda_studenti = Column(Integer, nullable=True)  # New column for student demand percentage

    numero_corsi = Column(String, nullable=True)
    percentuale_numero_corsi = Column(Integer, nullable=True)      # New column for number of courses percentage
    
    ricavo_medio = Column(String, nullable=True)
    ricavo_massimo = Column(String, nullable=True)

# Funzione asincrona per ottenere il db
async def get_db():
    async with SessionLocal() as db:
        yield db
