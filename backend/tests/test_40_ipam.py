from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

def testGetIpamRecords():
    response = client.get("/networks/2/ipam/")
    assert response.status_code == 200
    assert response.content.find(b"10.0.2.1") > -1
    assert response.content.find(b"10.0.2.254") > -1

# if no DHCP range exists, return 404
def testGetNonExistantDhcpRange():
    response = client.get("/networks/1/dhcp/14910")
    assert response.status_code == 404

# make a new DHCP range
def testNewDhcpRange():
    response = client.post("/networks/1/dhcp/", json={
        "name": "DHCP Test 1",
        "description": "Description 1",
        "startIp": "10.0.1.10",
        "endIp": "10.0.1.20"
    })

    if response.json() is not None:
        print(response.json())

    assert response.status_code == 201
    assert response.content.find(b"DHCP Test 1") > -1
    assert response.content.find(b"Description 1") > 1

# make a new DHCP range without a name
def testNewDhcpRangeWithoutAName():
    response = client.post("/networks/1/dhcp/", json={
        "description": "non-empty description",
        "startIp": "10.0.1.30",
        "endIp": "10.0.1.40"
    })

    assert response.status_code == 422

# make a new DHCP range without a description, this is valid
def testNewDhcpRangeWithoutDescription():
    response = client.post("/networks/1/dhcp/", json={
        "name": "DHCP Test 1",
        "startIp": "10.0.1.50",
        "endIp": "10.0.1.60"
    })

    assert response.status_code == 201
    assert response.content.find(b"DHCP Test 1") > -1

# read the new DHCP range
def testGetNewDhcpRange():
    response = client.get("/networks/1/dhcp/1")
    assert response.status_code == 200
    assert response.content.find(b"DHCP Test 1") > -1
    assert response.content.find(b"Description 1") > 1

# test deletion, it should return HTTP 204
def testDeleteDhcpRange():
    response = client.delete("/networks/1/dhcp/1")
    assert response.status_code == 204

# test the deletion again, it should produce a 404
def testDeleteDhcpRangeAgain():
    response = client.delete("/networks/1/dhcp/1")
    assert response.status_code == 404

# delete a DHCP range for a non-existent network
def testDeleteRangeNoNetwork():
    response = client.delete("/networks/292190/dhcp/1")
    assert response.status_code == 404

# test a new DHCP range where both input IPs are wrong
def testNewDhcpRangeBothIpsWrong():
    response = client.post("/networks/2/dhcp/", json={
        "name": "DHCP Test 2",
        "description": "Description 2",
        "startIp": "10.0.1.10",
        "endIp": "10.0.1.20"
    })

    if response.json() is not None:
        print(response.json())

    assert response.status_code == 400

# test a new DHCP range with wrong starting IP
def testNewDhcpRangeWrongStartingIp():
    response = client.post("/networks/2/dhcp/", json={
        "name": "DHCP Test 3",
        "description": "Description 3",
        "startIp": "10.0.1.10",
        "endIp": "10.0.2.20"
    })
    assert response.status_code == 400

# test a new DHCP range with the wrong ending IP
def testNewDhcpRangeWrongEndingIp():
    response = client.post("/networks/2/dhcp/", json={
        "name": "DHCP Test 4",
        "description": "Description 4",
        "startIp": "10.0.2.10",
        "endIp": "10.0.1.20"
    })
    assert response.status_code == 400
