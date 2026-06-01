from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert json_data["service"] == "IoT Telemetry Service"

def test_get_all_telemetry():
    response = client.get("/telemetry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert data[0]["sensor_id"] == "temp-sensor-01"

def test_post_telemetry():
    payload = {
        "sensor_id": "vibration-sensor-99",
        "type": "vibration",
        "value": 0.45,
        "unit": "g"
    }
    response = client.post("/telemetry", json=payload)
    # The API returns status_code 210 for created as per endpoint design
    assert response.status_code == 210
    data = response.json()
    assert data["sensor_id"] == "vibration-sensor-99"
    assert data["value"] == 0.45
    assert "timestamp" in data

def test_get_sensor_telemetry_success():
    response = client.get("/telemetry/humidity-sensor-01")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "humidity"
    assert data["unit"] == "%"

def test_get_sensor_telemetry_not_found():
    response = client.get("/telemetry/non-existent-sensor")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor non-existent-sensor not found"
