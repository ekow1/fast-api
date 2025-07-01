from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Dict, List
import os

app = FastAPI(
    title="FastAPI Service",
    description="A simple FastAPI service with uv, Docker, and AWS deployment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str = None
    price: float
    tax: float = None

# In-memory storage (use a database in production)
items_db: List[Dict] = []
item_counter = 0

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Service", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-service"}

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    global item_counter
    item_counter += 1
    item_dict = item.dict()
    item_dict["id"] = item_counter
    items_db.append(item_dict)
    return item_dict

@app.get("/items/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 100):
    return items_db[skip : skip + limit]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item["id"] != item_id]
    return {"message": f"Item {item_id} deleted"}

@app.get("/items/stats")
async def get_items_stats():
    """Get statistics about the items in the database"""
    if not items_db:
        return {
            "total_items": 0,
            "average_price": 0,
            "min_price": 0,
            "max_price": 0,
            "total_value": 0
        }
    
    prices = [item["price"] for item in items_db if item.get("price") is not None]
    total_value = sum(item["price"] + (item["tax"] or 0) for item in items_db if item.get("price") is not None)
    
    return {
        "total_items": len(items_db),
        "average_price": sum(prices) / len(prices) if prices else 0,
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "total_value": total_value
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
