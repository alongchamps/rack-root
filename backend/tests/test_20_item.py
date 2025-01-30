

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testMakeDeviceType():
    response = client.post("/deviceTypes/", json={"name": "Test device type"})
    assert response.status_code == 201

def testMakeDeviceType2():
    response = client.post("/deviceTypes/", json={"name": "Raspberry Pi"})
    assert response.status_code == 201

def testGettingItemThatDoesntExist():
    response = client.get("/items/2723987")
    assert response.status_code == 404

def testNewItem():
    response = client.post("/items/", json={
        "name": "testItem1",
        "description": "testDesc1",
        "deviceTypeId": 2,
        "serialNumber": "FOOB4R",
        "purchaseDate": "1970-01-01",
        "warrantyExpiration": "1971-01-01",
        "notes": "notes test"
        })
    assert response.status_code == 201

def testGetNewlyCreatedItem():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.content.find(b"testItem1") > 0
    assert response.content.find(b"testDesc1") > 0
    assert response.content.find(b"FOOB4R") > 0
    assert response.content.find(b"1970") > 0
    assert response.content.find(b"1971") > 0
    assert response.content.find(b"notes test") > 0
    assert response.content.find(b"Test device type") > 0

def testNewItem2():
    response = client.post("/items/", json={
        "name": "testItem2",
        "description": "testDesc2",
        "deviceTypeId": 2,
        "serialNumber": "B4RGLASS",
        "purchaseDate": "1972-01-01",
        "warrantyExpiration": "1973-01-01",
        "notes": "notes test 2"
        })
    assert response.status_code == 201

def testNewItemWrongDevice():
    response = client.post("/items/", json={
        "name": "testItem3",
        "description": "test description 3",
        "deviceTypeId": 47,
        "serialNumber": "B4RGLASS",
        "purchaseDate": "1974-01-01",
        "warrantyExpiration": "1975-01-01",
        "notes": "notes test 3"
        })
    assert response.status_code == 400

def testUpdateItem2():
    # test that the name updates and description stays the name
    response = client.patch("/items/2", json={"name": "item2test"})
    assert response.status_code == 202

    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.content.find(b"item2test") > -1
    assert response.content.find(b"testDesc2") > -1

    # opposite test - name does not update and description does
    response = client.patch("/items/2", json={"description": "newDescription2"})
    assert response.status_code == 202

    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.content.find(b"item2test") > -1
    assert response.content.find(b"newDescription2") > -1

def testUpdateItem3():
    response = client.patch("/items/2", json={"deviceTypeId": 3})
    assert response.status_code == 202

    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.content.find(b"Raspberry Pi") > -1

def testDevTypeDoesntExist():
    response = client.patch("/items/2", json={"deviceTypeId": 4})
    assert response.status_code == 400



# def testNewItem3():
#     response = client.post("/items/", json={"name": "item3","description": "description3"})
#     assert response.status_code == 201

# def testUpdateItemPut():
#     response = client.put("/items/3", json={"name": "item3test", "description": "item3desc"})
#     assert response.status_code == 202

#     response = client.get("/items/3")
#     assert response.status_code == 200
#     assert response.content.find(b"item3test") > 0
#     assert response.content.find(b"item3desc") > 0

#     #should fail with HTTP 422, this is only a partial update
#     response = client.put("/items/3", json={"name": "newName"})
#     assert response.status_code == 422

#     #should fail with HTTP 422, this is only a partial update
#     response = client.put("/items/3", json={"description": "newDescription2"})
#     assert response.status_code == 422

#     # response = client.get("/items/2")
#     # assert response.status_code == 200
#     # assert response.content.find(b"item2test") > 0
#     # assert response.content.find(b"newDescription2") > 0

# # test that we get back a valid respond when asking for all items
def testGetAllInventoryItems():
    response = client.get("/items/")
    assert response.status_code == 200

def testDeleteInventoryItem():
    response = client.delete("/items/2")
    assert response.status_code == 200

def testDeleteItemAgain():
    response = client.delete("/items/2")
    assert response.status_code == 404
