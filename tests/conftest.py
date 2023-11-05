import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from myapp.mymodels import Data1, Data2, Data3
from myapp.mymodels import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="module")
def test_db():
    # Создаем in-memory базу данных для тестов
    engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Создаем таблицы и заполняем данными
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for i in range(1, 61):
            if i <= 10 or (31 <= i <= 40):
                db.add(Data1(name=f"Data1 Row {i}"))
            elif i <= 20 or (41 <= i <= 50):
                db.add(Data2(name=f"Data2 Row {i}"))
            else:
                db.add(Data3(name=f"Data3 Row {i}"))
        db.commit()

    yield engine

    # Очищаем базу данных после завершения тестов
    Base.metadata.drop_all(bind=engine)
