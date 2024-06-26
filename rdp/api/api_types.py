from pydantic import BaseModel

class DeviceNoId(BaseModel):
    name : str
    description : str
    location_id: int

class Device(DeviceNoId):
    id : int

class LocationNoId(BaseModel):
    name : str
    description : str

class Location(LocationNoId):
    id : int

class ValueTypeNoID(BaseModel):
    type_name : str
    type_unit : str

class ValueType(ValueTypeNoID):
    id : int

class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float
    device_id: int

class Value(ValueNoID):
    id: int

class ApiDescription(BaseModel):
    description : str = "This is the Api"
    value_type_link : str = "/type"
    value_link : str = "/value"