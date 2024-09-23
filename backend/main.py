# Import necessary modules and classes
from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware

# imports for items
from .database import ItemResponse, ItemUpdate
from .item import read_all_items, read_item, create_item

# imports for device type 
from .database import DeviceTypeResponse
from .deviceType import read_all_device_types, create_device_type

# FastAPI app instance
app = FastAPI()

router = APIRouter()

# routes for handling items
router.add_api_route("/items/", read_all_items, methods=['GET'], response_model=list[ItemResponse])
router.add_api_route("/items/{item_id:int}", read_item, methods=['GET'], response_model=ItemResponse)
router.add_api_route("/items/", create_item, methods=['POST'], response_model=ItemResponse, status_code=status.HTTP_201_CREATED)

# routes for handling device types
router.add_api_route("/deviceTypes/", read_all_device_types, methods=['GET'], response_model=list[DeviceTypeResponse])
router.add_api_route("/deviceTypes/", create_device_type, methods=['POST'], response_model=DeviceTypeResponse, status_code=status.HTTP_201_CREATED)

app.include_router(router)

origins = [
    "http://localhost:443",
    "localhost:443",
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
