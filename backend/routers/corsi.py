from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas import CorsoCreate, Insight
from database import get_db, CorsoUdemy

router = APIRouter()

@router.get("/api/corsi")
async def get_corsi(db: AsyncSession = Depends(get_db)):
    query = select(CorsoUdemy)
    result = await db.execute(query)
    corsi = result.scalars().all()
    return [
        {
            "id": corso.id,
            "titolo": corso.titolo,
            "link": corso.link,
            "domanda": corso.domanda_studenti,
            "numero_corsi": corso.numero_corsi,
            "ricavo_medio": corso.ricavo_medio,
            "ricavo_massimo": corso.ricavo_massimo,
            "percentuale_domanda_studenti": corso.percentuale_domanda_studenti,
            "percentuale_numero_corsi": corso.percentuale_numero_corsi,
        }
        for corso in corsi
    ]

@router.post("/api/corsi")
async def add_corso(corso: CorsoCreate, db: AsyncSession = Depends(get_db)):
    nuovo_corso = CorsoUdemy(titolo=corso.titolo, link=corso.link)
    db.add(nuovo_corso)
    await db.commit()
    await db.refresh(nuovo_corso)
    return {"message": "Corso aggiunto con successo!"}

@router.delete("/api/corsi/{id}")
async def delete_corso(id: int, db: AsyncSession = Depends(get_db)):
    corso = await db.get(CorsoUdemy, id)
    if corso:
        await db.delete(corso)
        await db.commit()
        return {"message": "Corso eliminato"}
    raise HTTPException(status_code=404, detail="Corso non trovato")

@router.post("/api/insights", status_code=201)
async def create_insight(insight: Insight, db: AsyncSession = Depends(get_db)):
    query = select(CorsoUdemy).where(CorsoUdemy.titolo == insight.topic)
    result = await db.execute(query)
    matching_corsi = result.scalars().all()

    print(f"[DEBUG] Trovati {len(matching_corsi)} corsi con titolo: {insight.topic}")
    
    if len(matching_corsi) > 1:
        raise HTTPException(status_code=400, detail=f"Trovati {len(matching_corsi)} corsi con lo stesso titolo!")

    corso = matching_corsi[0] if matching_corsi else None

    if corso:
        corso.domanda_studenti = insight.student_demand
        corso.numero_corsi = insight.number_of_courses
        corso.ricavo_medio = insight.average_monthly_revenue
        corso.ricavo_massimo = insight.maximum_monthly_revenue
        corso.percentuale_domanda_studenti = insight.student_demand_percentage
        corso.percentuale_numero_corsi = insight.number_of_courses_percentage
        await db.commit()
        await db.refresh(corso)
        return {"message": "Insight aggiornato", "id": corso.id}
    else:
        nuovo = CorsoUdemy(
            titolo=insight.topic,
            link="",
            domanda_studenti=insight.student_demand,
            numero_corsi=insight.number_of_courses,
            ricavo_medio=insight.average_monthly_revenue,
            ricavo_massimo=insight.maximum_monthly_revenue,
            percentuale_domanda_studenti=insight.student_demand_percentage,
            percentuale_numero_corsi=insight.number_of_courses_percentage,
        )
        db.add(nuovo)
        await db.commit()
        await db.refresh(nuovo)
        return {"message": "Insight creato ex novo", "id": nuovo.id}
