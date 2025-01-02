# Import necessary modules and classes
from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware

# imports for items
# from .database import ItemResponse
from .validation_item import ItemResponse
from .item import read_all_items, read_item, create_item, update_item, delete_item

# imports for device type 
# from .database import DeviceTypeResponse
from .deviceType import read_all_device_types, read_device_type, create_device_type, update_device_type, delete_device_type
from .validation_deviceType import DeviceTypeResponse

# imports for subnets
from .subnet import read_all_subnets, read_single_subnet, create_subnet, delete_subnet, add_gateway, delete_gateway
from .validation_subnet import SubnetResponse # , SubnetUpdate

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
router.add_api_route("/deviceTypes/{dev_id:int}", delete_device_type, methods=['DELETE'])

# # # # # # # # # # # # # # # # # # # # # # # #
# routes for handling networking / IPAM stuff #
# # # # # # # # # # # # # # # # # # # # # # # #

# HTTP GET methods
router.add_api_route("/networks/", read_all_subnets, methods=['GET'], response_model=list[SubnetResponse])
router.add_api_route("/networks/{subnet_id:int}", read_single_subnet, methods=['GET'], response_model=SubnetResponse)

# HTTP POST new subnet
router.add_api_route("/networks/", create_subnet, methods=['POST'], response_model=SubnetResponse, status_code=status.HTTP_201_CREATED)

# HTTP DELETE subnet
router.add_api_route("/networks/{subnet_id:int}", delete_subnet, methods=['DELETE'])

# gateway related records
router.add_api_route("/networks/{subnet_id:int}/gateway", add_gateway, methods=['POST'], status_code=status.HTTP_201_CREATED)
router.add_api_route("/networks/{subnet_id:int}/gateway", delete_gateway, methods=['DELETE'], status_code=status.HTTP_200_OK)

# # # # # # # # # # # # #
# end HTTP methods here #
# # # # # # # # # # # # #

# add the router and set origins
app.include_router(router)
origins = [ "http://localhost:443", "localhost:443", "http://localhost:3000", "localhost:3000", ]
app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
