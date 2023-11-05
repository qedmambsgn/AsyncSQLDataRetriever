from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Data1(Base):
    __tablename__ = "data_1"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Data2(Base):
    __tablename__ = "data_2"
    id = Column(Integer, primary_key=True, )
    name = Column(String)

class Data3(Base):
    __tablename__ = "data_3"
    id = Column(Integer, primary_key=True)
    name = Column(String)