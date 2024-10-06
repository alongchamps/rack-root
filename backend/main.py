# Import necessary modules and classes
from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware

# imports for items
# from .database import ItemResponse
from .validation_item import ItemResponse
from .item import read_all_items, read_item, create_item, update_item, delete_item

# imports for device type 
# from .database import DeviceTypeResponse
from .validation_deviceType import DeviceTypeResponse
from .deviceType import read_all_device_types, read_device_type, create_device_type, update_device_type, delete_device_type

# FastAPI app instance
app = FastAPI()

router = APIRouter()

# # # # # # # # # # # # # # # # # # # # 
# routes for handling items
# # # # # # # # # # # # # # # # # # # # 
# HTTP GET methods for all items and single items
router.add_api_route("/items/", read_all_items, methods=['GET'], response_model=list[ItemResponse])
router.add_api_route("/items/{item_id:int}", read_item, methods=['GET'], response_model=ItemResponse)

# HTTP POST create new item
router.add_api_route("/items/", create_item, methods=['POST'], response_model=ItemResponse, status_code=status.HTTP_201_CREATED)

# HTTP PUT update item
router.add_api_route("/items/{item_id:int}", update_item, methods=['PATCH'], status_code=status.HTTP_202_ACCEPTED)

# HTTP DELETE a single inventory item
router.add_api_route("/items/{item_id:int}", delete_item, methods=['DELETE'], status_code=status.HTTP_200_OK)

# # # # # # # # # # # # # # # # # #
# routes for handling device types
# # # # # # # # # # # # # # # # # #

# HTTP GET methods for all device types and single device types
router.add_api_route("/deviceTypes/", read_all_device_types, methods=['GET'], response_model=list[DeviceTypeResponse])
router.add_api_route("/deviceTypes/{dev_id:int}", read_device_type, methods=['GET'], response_model=DeviceTypeResponse)

# HTTP POST new device type
router.add_api_route("/deviceTypes/", create_device_type, methods=['POST'], response_model=DeviceTypeResponse, status_code=status.HTTP_201_CREATED)

# HTTP PUT update single device type
router.add_api_route("/deviceTypes/{dev_id:int}", update_device_type, methods=['PUT'], status_code=status.HTTP_202_ACCEPTED)

# HTTP DELETE single device type
router.add_api_route("/deviceTypes/{dev_id:int}", delete_device_type, methods=['DELETE'] )


app.include_router(router)
origins = [ "http://localhost:443", "localhost:443", "http://localhost:3000", "localhost:3000", ]
app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
