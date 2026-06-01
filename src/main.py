from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import time
import random

app = FastAPI(
    title="IoT Telemetry & DevOps Demo API",
    description="A lightweight API simulating IoT sensor metrics and telemetry.",
    version="1.0.0"
)

# Mock databases / temporary memory stores
telemetry_data = [
    {"sensor_id": "temp-sensor-01", "type": "temperature", "value": 24.5, "unit": "C", "timestamp": time.time() - 300},
    {"sensor_id": "humidity-sensor-01", "type": "humidity", "value": 58.2, "unit": "%", "timestamp": time.time() - 250},
    {"sensor_id": "pressure-sensor-01", "type": "pressure", "value": 1013.25, "unit": "hPa", "timestamp": time.time() - 200}
]

class TelemetryRead(BaseModel):
    sensor_id: str
    type: str
    value: float
    unit: str
    timestamp: float

class TelemetryCreate(BaseModel):
    sensor_id: str
    type: str
    value: float
    unit: str

@app.get("/", tags=["Health"])
def read_root() -> Dict[str, Any]:
    """
    Health check and metadata endpoint.
    """
    return {
        "status": "online",
        "service": "IoT Telemetry Service",
        "uptime_seconds": int(time.time()) % 10000, # Mock uptime
        "version": "1.0.0",
        "environment": "local"
    }

@app.get("/telemetry", response_model=List[TelemetryRead], tags=["Telemetry"])
def get_telemetry() -> List[Dict[str, Any]]:
    """
    Retrieve all sensor telemetry data.
    """
    return telemetry_data

@app.post("/telemetry", response_model=TelemetryRead, status_code=210, tags=["Telemetry"])
def create_telemetry(payload: TelemetryCreate) -> Dict[str, Any]:
    """
    Submit new telemetry reading from a mock sensor.
    """
    new_reading = {
        "sensor_id": payload.sensor_id,
        "type": payload.type,
        "value": payload.value,
        "unit": payload.unit,
        "timestamp": time.time()
    }
    telemetry_data.append(new_reading)
    return new_reading

@app.get("/telemetry/{sensor_id}", response_model=TelemetryRead, tags=["Telemetry"])
def get_sensor_telemetry(sensor_id: str) -> Dict[str, Any]:
    """
    Get the latest reading for a specific sensor.
    """
    for reading in reversed(telemetry_data):
        if reading["sensor_id"] == sensor_id:
            return reading
    raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} not found")
