from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testGetIpamRecords():
    response = client.get("/networks/2/ipam")
    assert response.status_code == 200
