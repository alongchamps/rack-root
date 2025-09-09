from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

def testSearchNetworkNoResults():
    # find a random network that won't be in the database
    response = client.get("/search/networks/20.30")
    assert response.status_code == 200

    # look for no results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 0

def testSearchNetworkOneResult():
    # look for '10.0.2.0'
    response = client.get("/search/networks/10.0.2.0")
    assert response.status_code == 200

    # expect one result
    jsonData = json.loads(response.content)
    assert len(jsonData) == 1

def testSearchNetworkByName():
    # look for 'Intranet-10'
    response = client.get("/search/networks/Intranet-10")
    assert response.status_code == 200

    # expect one result
    jsonData = json.loads(response.content)
    assert len(jsonData) == 1

def testSearchNetworkTwoResults():
    # look for 'class-Int'
    response = client.get("/search/networks/class-Int")
    assert response.status_code == 200

    # expect two results
    jsonData = json.loads(response.content)
    assert len(jsonData) == 2
