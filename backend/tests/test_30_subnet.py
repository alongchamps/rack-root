from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testMakeSubnet():
    response = client.post("/networks/", json={
        "name": "Intranet-10",
        "vlan": 10,
        "classification": "class-Int",
        "network": "10.0.1.0",
        "subnetMaskBits": 24
    })
    assert response.status_code == 201

def testGetFirstSubnet():
    response = client.get("/networks/1")
    assert response.status_code == 200
    assert response.content.find(b"Intranet-10") > -1
    assert response.content.find(b"\"vlan\":10") > -1
    assert response.content.find(b"class-Int") > -1
    assert response.content.find(b"10.0.1.0") > -1
    assert response.content.find(b"24") > -1
    assert response.content.find(b"10.0.1.1") > -1
    assert response.content.find(b"10.0.1.254") > -1

def testGetNonExistentSubnet():
    response = client.get("/networks/2982982")
    assert response.status_code == 404

def testMakeSubnetWithWrongBits():
    response = client.post("/networks/", json={
        "name": "Intranet-10",
        "vlan": 10,
        "classification": "class-Int",
        "network": "10.0.0.2",
        "subnetMaskBits": 24
    })
    assert response.status_code == 400

def testOverlappingNetworks():
    response = client.post("/networks/", json={
        "name": "Intranet-20",
        "vlan": 20,
        "classification": "class-Int-20",
        "network": "10.0.1.128",
        "subnetMaskBits": 26
    })
    assert response.status_code == 400
    assert response.content.find(b"Networks must be unique.") > -1

def testNewNetwork2():
    response = client.post("/networks/", json={
        "name": "Test-intranet-2",
        "vlan": 2,
        "classification": "class-Int",
        "network": "10.0.2.0",
        "subnetMaskBits": 24
    })
    assert response.status_code == 201

def testGetSecondSubnet():
    response = client.get("/networks/2")
    assert response.status_code == 200
    assert response.content.find(b"Test-intranet-2") > -1
    assert response.content.find(b"\"vlan\":2") > -1
    assert response.content.find(b"class-Int") > -1
    assert response.content.find(b"10.0.2.0") > -1
    assert response.content.find(b"24") > -1

def testGatewayAddition():
    response = client.post("/networks/2/gateway/", json={
        "ipAddress": "10.0.2.253"
    })
    assert response.status_code == 201

def testReadingGateway():
    response = client.get("/networks/2/gateway/")
    assert response.content.find(b"10.0.2.253") > -1

def testGatewayDeletion():
    response = client.delete("/networks/2/gateway/")
    assert response.status_code == 204

def testGatewayMissing():
    response = client.get("/networks/2/gateway/")
    assert response.status_code == 404
    assert response.content.find(b"subnet.readGateway - No gateway on that network") > -1

def testChangingGateway():
    response = client.post("/networks/2/gateway/", json={
        "ipAddress": "10.0.2.1"
    })
    assert response.status_code == 201

    response = client.get("/networks/2/gateway/")
    assert response.content.find(b"10.0.2.1") > -1

def testReadAllSubnets():
    response = client.get("/networks/")
    assert response.status_code == 200
    assert response.content.find(b"Intranet-10") > -1
    assert response.content.find(b"Test-intranet-2") > -1

# check that the server does not accept an IP address outside of a network's range
def testGatewayNotInSubnet():
    response = client.post("/networks/2/gateway/", json={
        "ipAddress": "192.168.12.1"
    })
    assert response.status_code == 500
    
    #now check that the gateway didn't change
    response = client.get("/networks/2/gateway/")
    assert response.content.find(b"10.0.2.1") > -1

def testAddingDuplicateNetwork():
    response = client.post("/networks/", json={
        "name": "Test-intranet-2",
        "vlan": 2,
        "classification": "class-Int",
        "network": "10.0.2.0",
        "subnetMaskBits": 24
    })
    assert response.status_code == 400

def testDeleteSubnet():
    # make a network so we can delete the network
    # this is expected to come in with an ID of '3'
    response = client.post("/networks/", json={
        "name": "Deletion-Test",
        "vlan": 30,
        "classification": "delete-me",
        "network": "10.0.4.0",
        "subnetMaskBits": 24
    })
    assert response.status_code == 201

    # delete network 3
    response = client.delete("/networks/3")
    assert response.status_code == 204
