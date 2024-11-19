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

# Test successful vehicle creation
def test_add_vehicle_success(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["vin"] == "1HGBH41JXMN109186"

# Test adding vehicle with missing fields
def test_add_vehicle_missing_fields(client):
    payload = {"manufacturer": "Honda"}
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 422
    data = response.get_json()
    assert "Missing field" in data['error']

# Test adding a duplicate vehicle
def test_add_vehicle_duplicate_vin(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "UNIQUE constraint failed" in data['error']

# Test adding a vehicle with invalid data types
def test_add_vehicle_invalid_data(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": "invalid",  # Invalid type
        "model_name": "Civic",
        "model_year": "twenty twenty",  # Invalid type
        "purchase_price": "twenty thousand",  # Invalid type
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 400


# Test retrieving all vehicles
def test_get_vehicles(client):
    payload1 = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    payload2 = {
        "vin": "1HGCM82633A123456",
        "manufacturer": "Toyota",
        "horse_power": 200,
        "model_name": "Camry",
        "model_year": 2022,
        "purchase_price": 30000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload1)
    client.post('/vehicle', json=payload2)
    response = client.get('/vehicle')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

# Test retrieving a specific vehicle
def test_get_vehicle_success(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    response = client.get('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 200
    data = response.get_json()
    assert data["vin"] == "1HGBH41JXMN109186"

# Test retrieving a non-existent vehicle
def test_get_nonexistent_vehicle(client):
    response = client.get('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

# Test updating an existing vehicle
def test_update_vehicle_success(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    update_payload = {"horse_power": 180}
    response = client.put('/vehicle/1HGBH41JXMN109186', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["horse_power"] == 180

# Test updating a non-existent vehicle
def test_update_nonexistent_vehicle(client):
    response = client.put('/vehicle/INVALIDVIN', json={"manufacturer": "Nissan"})
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

# Test updating a vehicle with invalid data
def test_update_vehicle_invalid_data(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    update_payload = {"horse_power": "invalid"}
    response = client.put('/vehicle/1HGBH41JXMN109186', json=update_payload)
    assert response.status_code == 400


# Test deleting an existing vehicle
def test_delete_vehicle_success(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    response = client.delete('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 204

# Test deleting a non-existent vehicle
def test_delete_nonexistent_vehicle(client):
    response = client.delete('/vehicle/INVALIDVIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

# Test adding a vehicle with an empty payload
def test_add_vehicle_empty_payload(client):
    response = client.post('/vehicle', json={})
    assert response.status_code == 422
    data = response.get_json()
    assert "Missing field" in data['error']

# Test adding a vehicle with an invalid VIN length
def test_add_vehicle_invalid_vin_length(client):
    payload = {
        "vin": "1HGBH41",  # VIN too short
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid VIN" in data['error']

# Test adding a vehicle with special characters in VIN
def test_add_vehicle_special_characters_vin(client):
    payload = {
        "vin": "1HGBH41JXMN!@#$%",  # Invalid characters
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid VIN" in data['error']

# Test getting a vehicle with an invalid VIN format
def test_get_vehicle_invalid_vin_format(client):
    response = client.get('/vehicle/INVALID!VIN')
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

# Test retrieving all vehicles when no vehicles exist
def test_get_vehicles_empty(client):
    response = client.get('/vehicle')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0

# Test updating a vehicle with additional unexpected fields
def test_update_vehicle_extra_fields(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    update_payload = {"new_field": "unexpected_value"}
    response = client.put('/vehicle/1HGBH41JXMN109186', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "new_field" not in data  # Ensure unexpected fields are ignored


# Test deleting a vehicle that was already deleted
def test_delete_vehicle_already_deleted(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    client.delete('/vehicle/1HGBH41JXMN109186')  # First deletion
    response = client.delete('/vehicle/1HGBH41JXMN109186')  # Attempting second deletion
    assert response.status_code == 404
    data = response.get_json()
    assert "Vehicle not found" in data['error']

# Test adding a vehicle with minimum purchase price
def test_add_vehicle_min_purchase_price(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 0,  # Minimum valid price
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 201

# Test updating a vehicle with partial valid data
def test_update_vehicle_partial_data(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload)
    update_payload = {"fuel_type": "Electric"}
    response = client.put('/vehicle/1HGBH41JXMN109186', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["fuel_type"] == "Electric"
    assert data["manufacturer"] == "Honda"  # Ensure other fields are unchanged

# Test deleting all vehicles sequentially
def test_delete_all_vehicles(client):
    payload1 = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2020,
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    payload2 = {
        "vin": "1HGCM82633A123456",
        "manufacturer": "Toyota",
        "horse_power": 200,
        "model_name": "Camry",
        "model_year": 2022,
        "purchase_price": 30000,
        "fuel_type": "Gasoline"
    }
    client.post('/vehicle', json=payload1)
    client.post('/vehicle', json=payload2)

    # Delete both vehicles
    client.delete('/vehicle/1HGBH41JXMN109186')
    client.delete('/vehicle/1HGCM82633A123456')

    # Verify no vehicles remain
    response = client.get('/vehicle')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0

# Test adding a vehicle with a future model year
def test_add_vehicle_future_model_year(client):
    payload = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer": "Honda",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2030,  # Future year
        "purchase_price": 20000,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=payload)
    assert response.status_code == 201
