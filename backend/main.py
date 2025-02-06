# Import necessary modules and classes
from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware

# imports for different object types
from .deviceType import readAllDeviceTypes, readDeviceType, createDeviceType, updateDeviceType, deleteDeviceType
from .iprecords import getIpRecords
from .item import readAllItems, readItem, createItem, updateItem, deleteItem
from .subnet import readAllSubnets, readSingleSubnet, createSubnet, deleteSubnet, readGateway, setGateway, deleteGateway

# base database classes and validation classes for FastAPI
from .database import DeviceType, Item, Subnet
from .validation_deviceType import DeviceTypeCreate, DeviceTypeResponse, DeviceTypeUpdate
from .validation_iprecord import IpRecordResponse, IpRecordGateway
from .validation_item import ItemCreate, ItemUpdate, ItemResponse
from .validation_subnet import SubnetCreate, SubnetResponse

# FastAPI app instance
app = FastAPI()
router = APIRouter()

# # # # # # # # # # # # # # # # # #
# routes for handling device types
# # # # # # # # # # # # # # # # # #

# HTTP GET methods for all device types and single device types
router.add_api_route("/deviceTypes/", readAllDeviceTypes, methods=['GET'], response_model=list[DeviceTypeResponse])
router.add_api_route("/deviceTypes/{devId:int}", readDeviceType, methods=['GET'], response_model=DeviceTypeResponse)

# HTTP POST new device type
router.add_api_route("/deviceTypes/", createDeviceType, methods=['POST'], response_model=DeviceTypeCreate, status_code=status.HTTP_201_CREATED)

# HTTP PUT update single device type
router.add_api_route("/deviceTypes/{devId:int}", updateDeviceType, methods=['PUT'], response_model=DeviceTypeUpdate, status_code=status.HTTP_202_ACCEPTED)

# HTTP DELETE single device type
router.add_api_route("/deviceTypes/{devId:int}", deleteDeviceType, methods=['DELETE'], status_code=status.HTTP_204_NO_CONTENT)

# # # # # # # # # # # # # # 
# routes for handling items
# # # # # # # # # # # # # # 

# HTTP GET methods for all items and single items
router.add_api_route("/items/", readAllItems, methods=['GET'], response_model=list[ItemResponse])
router.add_api_route("/items/{itemId:int}", readItem, methods=['GET'], response_model=ItemResponse)

# HTTP POST create new item
router.add_api_route("/items/", createItem, methods=['POST'], response_model=ItemResponse, status_code=status.HTTP_201_CREATED)

# HTTP PUT update item
router.add_api_route("/items/{itemId:int}", updateItem, methods=['PATCH'], status_code=status.HTTP_202_ACCEPTED)

# HTTP DELETE a single inventory item
router.add_api_route("/items/{itemId:int}", deleteItem, methods=['DELETE'], status_code=status.HTTP_204_NO_CONTENT)

# # # # # # # # # # # # # # # # #
# # routes for handling networks
# # # # # # # # # # # # # # # # #

# HTTP GET methods
router.add_api_route("/networks/", readAllSubnets, methods=['GET'], response_model=list[SubnetResponse])
router.add_api_route("/networks/{subnetId:int}", readSingleSubnet, methods=['GET'], response_model=SubnetResponse)

# HTTP POST new subnet
router.add_api_route("/networks/", createSubnet, methods=['POST'], response_model=SubnetCreate, status_code=status.HTTP_201_CREATED)

# HTTP DELETE subnet
router.add_api_route("/networks/{subnetId:int}", deleteSubnet, methods=['DELETE'], status_code=status.HTTP_204_NO_CONTENT)

# gateway related routes
router.add_api_route("/networks/{subnetId:int}/gateway/", readGateway, methods=['GET'], response_model=IpRecordResponse, status_code=status.HTTP_200_OK)
router.add_api_route("/networks/{subnetId:int}/gateway/", setGateway, methods=['POST'], response_model=IpRecordGateway, status_code=status.HTTP_201_CREATED)
router.add_api_route("/networks/{subnetId:int}/gateway/", deleteGateway, methods=['DELETE'], status_code=status.HTTP_204_NO_CONTENT)

# # # # # # # # # # # # # # #
# # routes for handling IPAM
# # # # # # # # # # # # # # #

# get all IPs for a network
router.add_api_route("/networks/{subnetId:int}/ipam", getIpRecords, methods=['GET'], response_model=list[IpRecordResponse], status_code=status.HTTP_200_OK)

# TODO add route here for handling DHCP range(s)?

# make new DHCP range
# router.add_api_route("/networks/{subnetId:int}/dhcp", createDhcpRange, methods=['POST'], status_code=status.HTTP_201_CREATED)
# I need parameters here for the start and end addresses

# delete DHCP range
# router.add_api_route("/networks/{subnetId:int}/dhcp", deleteDhcpRange, methods=['DELETE'], status_code=status.HTTP_204_NO_CONTENT)
# I need parameters here for the start and end addresses

# # # # # # # # # # # # #
# end HTTP methods here #
# # # # # # # # # # # # #

# add the router and set origins
app.include_router(router)
origins = [ "http://localhost:443", "localhost:443", "http://localhost:3000", "localhost:3000", ]
app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# TODO
# deleting a subnet deletes all associated records (via fkey) in the iprecords table
# figuring out DHCP related parameters/inputs - yet another class?
