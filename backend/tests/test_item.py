# invocation: pytest --import-mode prepend -c ./backend/tests/pytest.ini -v

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testGettingItemThatDoesntExist():
    response = client.get("/items/2723987")
    assert response.status_code == 404

# def testNewItem():
#     response = client.post("/items/", json={"name": "hello","description": "world"})
#     assert response.status_code == 201

# def testGetNewlyCreatedItem():
#     response = client.get("/items/1")
#     assert response.status_code == 200
#     assert response.content.find(b"hello") > 0
#     assert response.content.find(b"world") > 0

# def testNewItem2():
#     response = client.post("/items/", json={"name": "item2","description": "description2"})
#     assert response.status_code == 201

# def testGetNewlyCreatedItem2():
#     response = client.get("/items/2")
#     assert response.status_code == 200
#     assert response.content.find(b"item2") > 0
#     assert response.content.find(b"description2") > 0

# def testUpdateItem2():
#     response = client.patch("/items/2", json={"name": "item2test"})
#     assert response.status_code == 202

#     response = client.get("/items/2")
#     assert response.status_code == 200
#     assert response.content.find(b"item2test") > 0
#     assert response.content.find(b"description2") > 0

#     response = client.patch("/items/2", json={"description": "newDescription2"})
#     assert response.status_code == 202

#     response = client.get("/items/2")
#     assert response.status_code == 200
#     assert response.content.find(b"item2test") > 0
#     assert response.content.find(b"newDescription2") > 0

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

# # test that we get back a valid respond when asking for '/items/'
# def testGetAllInventoryItems():
#     response = client.get("/items/")
#     assert response.status_code == 200

# def testDeleteInventoryItem():
#     response = client.delete("/items/1")
#     assert response.status_code == 200

# def testDeleteItemAgain():
#     response = client.delete("/items/1")
#     assert response.status_code == 404
