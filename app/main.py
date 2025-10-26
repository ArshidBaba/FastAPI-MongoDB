from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import collection
from models import Item
from bson import ObjectId
from bson import ObjectId, errors as bson_errors

app = FastAPI()

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    result = await collection.insert_one(item.dict())
    item.id = str(result.inserted_id)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    items = []
    async for item in collection.find():
        item["id"] = str(item["_id"])
        del item["_id"]  # 👈 remove ObjectId to avoid validation error
        items.append(Item(**item))
    return items


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    try:
        obj_id = ObjectId(item_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid item ID format")

    item = await collection.find_one({"_id": obj_id})
    if item:
        item["id"] = str(item["_id"])
        del item["_id"]
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    result = await collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": item.dict(exclude={"id"})}
    )
    if result.modified_count:
        item.id = item_id
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")