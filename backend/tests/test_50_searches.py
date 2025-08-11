import json.scanner
from fastapi.testclient import TestClient
from backend.main import app
import json
import pytest

client = TestClient(app)

def testSearchItemNoResults():
    # find a random string that won't be in the database
    response = client.get("/search/items/KV9q82js")
    assert response.status_code == 200

    # look for no results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 0

def testSearchItemNewItem():
    response = client.post("/items/", json={
        "name": "rG3YAV",
        "description": "search test",
        "deviceTypeId": 2,
        "serialNumber": "g00g13",
        "purchaseDate": "1970-06-03T04:00:00.000Z",
        "warrantyExpiration": "1971-06-03T04:00:00.000Z",
        "notes": "notes test"
        })
    assert response.status_code == 201

def testSearchItemOneResult():
    response = client.get("/search/items/rG3YAV")
    assert response.status_code == 200

    # look for one result
    jsonData = json.loads(response.content)
    assert len(jsonData) == 1

def testSearchItemNewItem2():
    response = client.post("/items/", json={
        "name": "asdfghjkl",
        "description": "search test",
        "deviceTypeId": 2,
        "serialNumber": "g00g13",
        "purchaseDate": "1970-06-03T04:00:00.000Z",
        "warrantyExpiration": "1971-06-03T04:00:00.000Z",
        "notes": "notes test"
        })
    assert response.status_code == 201

def testSearchItemTwoResults():
    response = client.get("/search/items/search test")
    assert response.status_code == 200

    # look for two results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 2
