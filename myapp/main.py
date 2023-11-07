from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from myapp.mymodels import Base, Data1, Data2, Data3
from sqlalchemy import select
import asyncio

app = FastAPI()

# Создаем SQLAlchemy асинхронный движок
async_engine = create_async_engine("postgresql+asyncpg://postgres:qwerty@localhost/async_data_sources", echo=True, connect_args={"command_timeout": 2})

# Создаем сессию SQLAlchemy
Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    """Initialize models"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def fill_database():
    """Filling databases with some data according to the specified ID ranges"""
    async with Session() as session:
        data1_values = [{"id": i, "name": f"Data1 Row {i}"} for i in range(1, 11)] + [
            {"id": i, "name": f"Data1 Row {i}"} for i in range(31, 41)]
        data2_values = [{"id": i, "name": f"Data2 Row {i}"} for i in range(11, 21)] + [
            {"id": i, "name": f"Data2 Row {i}"} for i in range(41, 51)]
        data3_values = [{"id": i, "name": f"Data3 Row {i}"} for i in range(21, 31)] + [
            {"id": i, "name": f"Data3 Row {i}"} for i in range(51, 61)]

        await session.execute(Data1.__table__.insert().values(data1_values))
        await session.execute(Data2.__table__.insert().values(data2_values))
        await session.execute(Data3.__table__.insert().values(data3_values))

        await session.commit()


@app.on_event("startup")
async def on_startup():
    """Actions on application startup"""
    await init_models()
    await fill_database()


async def get_data_from_table(table: Base, session: Session):
    """Form a complex number.

    Parameters:
    table -- data table from where to extract
    session -- current open session with executable cursor
    """
    try:
        data = await session.execute(select(table))
    except:
        data = []
    return data


@app.get("/data", response_model=list[dict])
async def get_data():
    """GET Endpoint to get data from all tables; Sort result by ID"""
    async with Session() as session:
        data1, data2, data3 = await asyncio.gather(
            get_data_from_table(Data1, session),
            get_data_from_table(Data2, session),
            get_data_from_table(Data3, session)
        )

        await session.commit()

        data = []
        if data1:
            data.extend([{"id": row.id, "name": row.name} for row in data1.scalars()])
        if data2:
            data.extend([{"id": row.id, "name": row.name} for row in data2.scalars()])
        if data3:
            data.extend([{"id": row.id, "name": row.name} for row in data3.scalars()])

        data.sort(key=lambda item: item['id'])
        return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
