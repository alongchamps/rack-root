from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

def testMissingDhcpRange():
    # look for a record that's not in the database
    response = client.get("/search/dhcpRanges/asdfghjkl")
    assert response.status_code == 200

    # confirm no results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 0

def testSingleDhcpSearchResultByName():
    # look for 'DHCP Test 2'
    response = client.get("/search/dhcpRanges/DHCP Test 2")
    assert response.status_code == 200

    # confirm one results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 1

def testSingelDhcpSearchResultByDescription():
    # look for 'search testing'
    response = client.get("/search/dhcpRanges/search testing")
    assert response.status_code == 200

    # confirm one results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 1

def testTwoSearchResultsByName():
    # look for 'DHCP Test' which should be in two records
    response = client.get("/search/dhcpRanges/DHCP Test")
    assert response.status_code == 200

    # confirm one results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 2
