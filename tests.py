import pytest
from app import app, db, Vehicle

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_vehicle_missing_fields(client):
    payload = {
        "manufacturer": "Honda"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 422
    data = response.get_json()
    assert "Missing field" in data['error']

def test_add_vehicle_duplicate_vin(client):
    client.post('/vehicle', json={
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    })
    response = client.post('/vehicle', json={
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Toyota",
        "horse_power": 180,
        "model_name": "Corolla",
        "model_year": 2021,
        "purchase_price": 22000,
        "fuel_type": "Gasoline"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "UNIQUE constraint failed" in data['error']

def test_get_nonexistent_vehicle(client):
    response = client.get('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

def test_update_nonexistent_vehicle(client):
    response = client.put('/vehicle/INVALIDVIN', json={"manufacturer": "Nissan"})
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

def test_delete_nonexistent_vehicle(client):
    response = client.delete('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

def test_add_vehicle_missing_fields(client):
    payload = {
        "manufacturer": "Honda"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 422
    data = response.get_json()
    assert "Missing field" in data['error']

def test_add_vehicle_duplicate_vin(client):
    client.post('/vehicle', json={
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    })
    response = client.post('/vehicle', json={
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Toyota",
        "horse_power": 180,
        "model_name": "Corolla",
        "model_year": 2021,
        "purchase_price": 22000,
        "fuel_type": "Gasoline"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "UNIQUE constraint failed" in data['error']

def test_get_nonexistent_vehicle(client):
    response = client.get('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

def test_update_nonexistent_vehicle(client):
    response = client.put('/vehicle/INVALIDVIN', json={"manufacturer": "Nissan"})
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

def test_delete_nonexistent_vehicle(client):
    response = client.delete('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

