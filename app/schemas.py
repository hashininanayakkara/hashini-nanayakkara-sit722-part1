from pydantic import BaseModel

class InventoryBase(BaseModel):
    item_name: str
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryInDB(InventoryBase):
    id: int

    class Config:
        orm_mode = True
