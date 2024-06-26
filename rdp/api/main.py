from typing import Union, List

from fastapi import FastAPI, HTTPException

from rdp.sensor import Reader
from rdp.crud import create_engine, Crud
from . import api_types as ApiTypes
import logging

logger = logging.getLogger("rdp.api")
app = FastAPI()

@app.get("/")
def read_root() -> ApiTypes.ApiDescription:
    """This url returns a simple description of the api

    Returns:
        ApiTypes.ApiDescription: the Api description in json format 
    """    
    return ApiTypes.ApiDescription()

@app.get("/device/{id}/")
def read_device(id: int) -> ApiTypes.Device:
    """returns an explicit device identified by id

    Args:
        id (int): primary key of the desired device

    Raises:
        HTTPException: Thrown if a device with the given id cannot be accessed

    Returns:
        ApiTypes.Device: the desired device
    """
    global crud
    try:
         return crud.get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/device/{id}/values")
def read_device_values(id: int) -> List[ApiTypes.Value]:
    """returns all values from an explicit device

    Args:
        id (int): primary key of the desired device

    Raises:
        HTTPException: Thrown if a device with the given id cannot be accessed

    Returns:
        ApiTypes.Device: the desired device
    """
    global crud
    try:
         return crud.get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/devices/")
def read_devices() -> List[ApiTypes.Device]:
    """returns all devices

    Raises:
        HTTPException: Thrown if a device with the given id cannot be accessed

    Returns:
        ApiTypes.Device: the desired device
    """
    global crud
    try:
         return crud.get_devices()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/devices/{id}/values/")
def read_values_by_device(id: int) -> List[ApiTypes.Value]:
    """returns all values from one device

    Raises:
        HTTPException: Thrown if a device with the given id cannot be accessed

    Returns:
        ApiTypes.Device: the desired device
    """
    global crud
    try:
         return crud.get_values_by_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.post("/device/")
def post_device(device_name:str, device_description:str) -> ApiTypes.Device:
    """Implements the post of a new device

    Args:
        device_name (str): name of the new device
        device_description (str): description of the new device

    Returns:
        ApiTypes.Device: newly created device
    """
    global crud
    try:
        device_id = crud.add_or_update_device(device_name=device_name, device_description=device_description)
        return read_device(device_id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/location/{id}/")
def read_location(id: int) -> ApiTypes.Location:
    """returns an explicit location identified by id

    Args:
        id (int): primary key of the desired location

    Raises:
        HTTPException: Thrown if a location with the given id cannot be accessed

    Returns:
        ApiTypes.Location: the desired location
    """
    global crud
    try:
         return crud.get_location(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/locations/")
def read_locations() -> List[ApiTypes.Location]:
    """returns all locations

    Raises:
        HTTPException: Thrown if a location with the given id cannot be accessed

    Returns:
        ApiTypes.Location: the desired location
    """
    global crud
    try:
         return crud.get_locations()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/type/")
def read_types() -> List[ApiTypes.ValueType]:
    """Implements the get of all value types

    Returns:
        List[ApiTypes.ValueType]: list of available valuetypes. 
    """    
    global crud
    return crud.get_value_types()

@app.get("/type/{id}/")
def read_type(id: int) -> ApiTypes.ValueType:
    """returns an explicit value type identified by id

    Args:
        id (int): primary key of the desired value type

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ApiTypes.ValueType: the desired value type 
    """
    global crud
    try:
         return crud.get_value_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.put("/type/{id}/")
def put_type(id, value_type: ApiTypes.ValueTypeNoID) -> ApiTypes.ValueType:
    """PUT request to a special valuetype. This api call is used to change a value type object.

    Args:
        id (int): primary key of the requested value type
        value_type (ApiTypes.ValueTypeNoID): json object representing the new state of the value type. 

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed 

    Returns:
        ApiTypes.ValueType: the requested value type after persisted in the database. 
    """
    global crud
    try:
        crud.add_or_update_value_type(id, value_type_name=value_type.type_name, value_type_unit=value_type.type_unit)
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/value/{id}/")
def get_value(id: int) -> ApiTypes.Value:
    """returns an explicit value identified by id

    Args:
        id (int): primary key of the desired value

    Raises:
        HTTPException: Thrown if a value with the given id cannot be accessed

    Returns:
        ApiTypes.Location: the desired value
    """
    global crud
    try:
         return crud.get_value(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 

@app.get("/value/")
def get_values(type_id:int=None, device_id:int=None, start:int=None, end:int=None) -> List[ApiTypes.Value]:
    """Get values from the database. The default is to return all available values. This result can be filtered.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        List[ApiTypes.Value]: _description_
    """
    global crud
    try:
        values = crud.get_values(type_id, device_id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")

@app.post("/value/")
def post_value(value_time: int, value_type_id: int, value: float, device_id: int) -> ApiTypes.Value:
    """Implements the post of a new value

    Args:
        value_time (int): name of the new device
        value_type_id (int): description of the new device
        value (float): the actual value
        device_id (int): the devices' id

    Returns:
        ApiTypes.Device: newly created device
    """
    global crud
    try:
        value_id = crud.add_value(value_time, value_type_id, value, device_id)
        return get_value(value_id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.on_event("startup")
async def startup_event() -> None:
    """start the character device reader
    """    
    logger.info("STARTUP: Sensor reader!")
    global reader, crud
    engine = create_engine("sqlite:///rdb.test.db")
    crud = Crud(engine)
    reader = Reader(crud)
    reader.start()
    logger.debug("STARTUP: Sensor reader completed!")

@app.on_event("shutdown")
async def shutdown_event():
    """stop the character device reader
    """    
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")
