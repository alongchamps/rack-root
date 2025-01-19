# invocation: pytest --import-mode prepend -c ./backend/tests/pytest.ini -v

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testGetDeviceTypeThatDoesntExist():
    response = client.get("/deviceTypes/2723987")
    assert response.status_code == 404

def testNewDeviceType():
    response = client.post("/deviceTypes/", json={"name": "testDevice1"})
    assert response.status_code == 201

def testGetNewDevice():
    response = client.get("/deviceTypes/1")
    assert response.status_code == 200
    assert response.content.find(b"testDevice1") > 0

def testUpdateDevice():
    response = client.put("/deviceTypes/1", json={"name": "newTestDeviceName"})
    assert response.status_code == 202

def testGetUpdatedDevice():
    response = client.get("/deviceTypes/1")
    assert response.status_code == 200
    assert response.content.find(b"newTestDeviceName") > 0

def testDeleteDevice():
    response = client.delete("/deviceTypes/1")
    assert response.status_code == 200

def testDelete404():
    response = client.delete("/deviceTypes/1")
    assert response.status_code == 404
