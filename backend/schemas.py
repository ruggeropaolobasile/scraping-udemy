# backend/schemas.py
# Pydantic v2.10.6
from pydantic import BaseModel
from typing import Optional


class CorsoBase(BaseModel):
    titolo: str
    link: str

class CorsoCreate(CorsoBase):
    pass

class CorsoUpdate(BaseModel):
    domanda: Optional[str] = None
    numero_corsi: Optional[str] = None
    ricavo_medio: Optional[str] = None
    ricavo_massimo: Optional[str] = None
    percentuale_domanda_studenti: Optional[str] = None
    percentuale_numero_corsi: Optional[str] = None


class CorsoOut(CorsoBase):
    id: int
    domanda: Optional[str]
    numero_corsi: Optional[str]
    ricavo_medio: Optional[str]
    ricavo_massimo: Optional[str]
    percentuale_domanda_studenti: Optional[str]
    percentuale_numero_corsi: Optional[str]

class Insight(BaseModel):
    topic: str
    student_demand: str
    number_of_courses: str
    average_monthly_revenue: str
    maximum_monthly_revenue: str
    student_demand_percentage: int
    number_of_courses_percentage: int

    # Nuovo stile per Pydantic v2
    model_config = {
        "from_attributes": True
    }

class Config:
    from_attributes = True

class ArgomentoBase(BaseModel):
    nome: str

class ArgomentoOut(ArgomentoBase):
    id: int

    class Config:
        orm_mode = True