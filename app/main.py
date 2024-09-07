from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from models import Inventory, Base
from schemas import InventoryBase, InventoryCreate, InventoryInDB, InventoryUpdate
from db import engine, get_db

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Endpoint to create a new inventory item
@app.post("/inventories/", response_model=InventoryInDB)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Endpoint to retrieve an inventory item by ID
@app.get("/inventories/{inventory_id}", response_model=InventoryInDB)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

# Endpoint to retrieve all inventory items
@app.get("/inventories/", response_model=List[InventoryInDB])
def get_all_inventories(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

# Endpoint to update an inventory item by ID
@app.put("/inventories/{inventory_id}", response_model=InventoryInDB)
def update_inventory(inventory_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    for field, value in inventory.dict().items():
        setattr(db_inventory, field, value)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

# Endpoint to delete an inventory item by ID
@app.delete("/inventories/{inventory_id}", response_model=InventoryInDB)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    db.delete(db_inventory)
    db.commit()
    return db_inventory
