from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.clothing import ClothingItem
from app.schemas.clothing import ClothingCreate, ClothingResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items", response_model=ClothingResponse)
def create_item(item: ClothingCreate, db: Session = Depends(get_db)):
    db_item = ClothingItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items", response_model=list[ClothingResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(ClothingItem).all()


@router.get("/items/{item_id}", response_model=ClothingResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(ClothingItem).filter(ClothingItem.id == item_id).first()

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

@router.put("/items/{item_id}", response_model=ClothingResponse)
def update_item(item_id: int, updated: ClothingCreate, db: Session = Depends(get_db)):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()
    for key, value in updated.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/items/{item_id}/wash", response_model=ClothingResponse)
def cycle_wash_status(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()
    cycle = {"clean": "worn_once", "worn_once": "needs_wash", "needs_wash": "clean"}
    item.wash_status = cycle[item.wash_status]
    if item.wash_status == "worn_once":
        item.wear_count += 1
    db.commit()
    db.refresh(item)
    return item