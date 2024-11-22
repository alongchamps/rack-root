from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testMakeSubnet():
    response = client.post("/subnets/", json={
        "name": "Intranet-10",
        "vlan": 10,
        "classification": "class-Int",
        "network": "10.0.1.0",
        "subnetMaskBits": "24"
    })
    assert response.status_code == 201

def testGetFirstSubnet():
    response = client.get("/subnets/1")
    assert response.status_code == 200
    assert response.content.find(b"Intranet-10") > -1
    assert response.content.find(b"\"vlan\":10") > -1
    assert response.content.find(b"class-Int") > -1
    assert response.content.find(b"10.0.1.0") > -1
    assert response.content.find(b"24") > -1

def testGetNonExistentSubnet():
    response = client.get("/subnets/2982982")
    assert response.status_code == 404

def testMakeSubnetWithWrongBits():
    response = client.post("/subnets/", json={
        "name": "Intranet-10",
        "vlan": 10,
        "classification": "class-Int",
        "network": "10.0.0.2",
        "subnetMaskBits": "24"
    })
    assert response.status_code == 400

def testOverlappingNetworks():
    response = client.post("/subnets/", json={
        "name": "Intranet-20",
        "vlan": 20,
        "classification": "class-Int-20",
        "network": "10.0.1.128",
        "subnetMaskBits": "26"
    })
    assert response.status_code == 400
    assert response.content.find(b"Networks must be unique.") > -1
