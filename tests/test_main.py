import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)


def test_get_data(test_db):
    """Test data was fetched successfully"""
    print("Running test_get_data...")
    assert client.get("/data").status_code == 200
    print("test_get_data completed.")


def test_get_data_id(test_db):
    """Test data was sorted by ID"""
    print("Running test_get_data_id...")
    data = client.get("/data").json()
    ids = [item["id"] for item in data]
    assert ids == sorted(ids)
    print("test_get_data_id completed.")



def test_get_data_with_error(test_db):
    """Test data was fetched even if one table had an error"""
    with test_db.connect() as connection:
        connection.execute(text("DROP TABLE data_2"))
    print("Running test_get_data_with_error...")
    response = client.get("/data")
    assert response.status_code == 200  # Ожидаем ошибку 200
    print("test_get_data_with_error completed.")
