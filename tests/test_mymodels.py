
import pytest
from myapp.mymodels import Data1, Data2, Data3
from sqlalchemy import text

def test_data1(test_db):
    """Test data_1 table exists"""
    with test_db.connect() as connection:
        assert connection.execute(text("SELECT name FROM data_1 LIMIT 1")).scalar() is not None

def test_data2(test_db):
    """Test data_2 table exists"""
    with test_db.connect() as connection:
        assert connection.execute(text("SELECT name FROM data_2 LIMIT 1")).scalar() is not None

def test_data3(test_db):
    """Test data_3 table exists"""
    with test_db.connect() as connection:
        assert connection.execute(text("SELECT name FROM data_3 LIMIT 1")).scalar() is not None
