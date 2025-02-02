from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .init_models import Car, Detail, Change, SessionLocal

basic_router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models for request bodies
class CarCreate(BaseModel):
    owner: str
    brand: str
    appearance: str
    power: int
    max_speed: int
    created_at: date


class DetailCreate(BaseModel):
    name: str
    car_part: str
    firm: str
    price: float
    guarantee: date


class ChangeCreate(BaseModel):
    car_id: int
    mechanic_name: str
    issue_date: date
    appearance_change: int
    max_speed_change: int
    power_change: int


# CRUD operations for Cars
@basic_router.post("/cars/")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@basic_router.get("/cars/")
def read_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()


@basic_router.get("/cars/{car_id}")
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@basic_router.put("/cars/{car_id}")
def update_car(car_id: int, car: CarCreate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    for key, value in car.model_dump().items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)
    return db_car


@basic_router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}


# CRUD operations for Details
@basic_router.post("/details/")
def create_detail(detail: DetailCreate, db: Session = Depends(get_db)):
    db_detail = Detail(**detail.model_dump())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail


@basic_router.get("/details/")
def read_details(db: Session = Depends(get_db)):
    return db.query(Detail).all()


@basic_router.get("/details/{detail_id}")
def read_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")
    return db_detail


@basic_router.put("/details/{detail_id}")
def update_detail(detail_id: int, detail: DetailCreate, db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")

    for key, value in detail.model_dump().items():
        setattr(db_detail, key, value)

    db.commit()
    db.refresh(db_detail)
    return db_detail


@basic_router.delete("/details/{detail_id}")
def delete_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")

    db.delete(db_detail)
    db.commit()
    return {"message": "Detail deleted"}


# CRUD operations for Changes
@basic_router.post("/changes/")
def create_change(change: ChangeCreate, db: Session = Depends(get_db)):
    db_change = Change(**change.model_dump())
    db.add(db_change)
    db.commit()
    db.refresh(db_change)
    return db_change


@basic_router.get("/changes/")
def read_changes(db: Session = Depends(get_db)):
    return db.query(Change).all()


@basic_router.get("/changes/{change_id}")
def read_change(change_id: int, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")
    return db_change


@basic_router.put("/changes/{change_id}")
def update_change(change_id: int, change: ChangeCreate, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    for key, value in change.model_dump().items():
        setattr(db_change, key, value)

    db.commit()
    db.refresh(db_change)
    return db_change


@basic_router.delete("/changes/{change_id}")
def delete_change(change_id: int, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    db.delete(db_change)
    db.commit()
    return {"message": "Change deleted"}
