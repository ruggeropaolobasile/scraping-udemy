# crud.py
# 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import CorsoUdemy
from schemas import CorsoCreate, Insight


async def get_all_corsi(db: AsyncSession):
    result = await db.execute(select(CorsoUdemy))
    return result.scalars().all()


async def get_corso_by_id(db: AsyncSession, corso_id: int):
    return await db.get(CorsoUdemy, corso_id)


async def get_corso_by_titolo(db: AsyncSession, titolo: str):
    result = await db.execute(select(CorsoUdemy).where(CorsoUdemy.titolo == titolo))
    return result.scalar_one_or_none()


async def create_corso(db: AsyncSession, corso: CorsoCreate):
    nuovo_corso = CorsoUdemy(titolo=corso.titolo, link=corso.link)
    db.add(nuovo_corso)
    await db.commit()
    await db.refresh(nuovo_corso)
    return nuovo_corso


async def delete_corso(db: AsyncSession, corso_id: int):
    corso = await get_corso_by_id(db, corso_id)
    if corso:
        await db.delete(corso)
        await db.commit()
    return corso


async def upsert_insight(db: AsyncSession, insight: Insight):
    corso = await get_corso_by_titolo(db, insight.topic)
    if corso:
        corso.domanda_studenti = insight.student_demand
        corso.numero_corsi = insight.number_of_courses
        corso.ricavo_medio = insight.average_monthly_revenue
        corso.ricavo_massimo = insight.maximum_monthly_revenue
        corso.percentuale_domanda_studenti = insight.student_demand_percentage
        corso.percentuale_numero_corsi = insight.number_of_courses_percentage
        await db.commit()
        await db.refresh(corso)
        return corso, False
    else:
        nuovo = CorsoUdemy(
            titolo=insight.topic,
            link="",
            domanda_studenti=insight.student_demand,
            numero_corsi=insight.number_of_courses,
            ricavo_medio=insight.average_monthly_revenue,
            ricavo_massimo=insight.maximum_monthly_revenue,
            percentuale_domanda_studenti=insight.student_demand_percentage,
            percentuale_numero_corsi=insight.number_of_courses_percentage
        )
        db.add(nuovo)
        await db.commit()
        await db.refresh(nuovo)
        return nuovo, True