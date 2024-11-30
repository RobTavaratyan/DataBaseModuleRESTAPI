from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from init_models import Car, Detail, Change, SessionLocal, engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cars/")
def create_car(owner: str, brand: str, appearance: str, power: int, max_speed: int, created_at: date,
               db: Session = Depends(get_db)):
    db_car = Car(owner=owner, brand=brand, appearance=appearance, power=power, max_speed=max_speed,
                 created_at=created_at)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.get("/cars/")
def read_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()


@app.get("/cars/{car_id}")
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.put("/cars/{car_id}")
def update_car(car_id: int, owner: str, brand: str, appearance: str, power: int, max_speed: int,
               db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db_car.owner = owner
    db_car.brand = brand
    db_car.appearance = appearance
    db_car.power = power
    db_car.max_speed = max_speed

    db.commit()
    db.refresh(db_car)
    return db_car


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}


@app.post("/details/")
def create_detail(name: str, car_part: str, firm: str, price: float, guarantee: date, db: Session = Depends(get_db)):
    db_detail = Detail(name=name, car_part=car_part, firm=firm, price=price, guarantee=guarantee)
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail


@app.get("/details/")
def read_details(db: Session = Depends(get_db)):
    return db.query(Detail).all()


@app.get("/details/{detail_id}")
def read_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")
    return db_detail


@app.put("/details/{detail_id}")
def update_detail(detail_id: int, name: str, car_part: str, firm: str, price: float, guarantee: date,
                  db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")

    db_detail.name = name
    db_detail.car_part = car_part
    db_detail.firm = firm
    db_detail.price = price
    db_detail.guarantee = guarantee

    db.commit()
    db.refresh(db_detail)
    return db_detail


@app.delete("/details/{detail_id}")
def delete_detail(detail_id: int, db: Session = Depends(get_db)):
    db_detail = db.query(Detail).filter(Detail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Detail not found")

    db.delete(db_detail)
    db.commit()
    return {"message": "Detail deleted"}


@app.post("/changes/")
def create_change(car_id: int, mechanic_name: str, issue_date: date, appearance_change: int, max_speed_change: int,
                  power_change: int, db: Session = Depends(get_db)):
    db_change = Change(
        car_id=car_id,
        mechanic_name=mechanic_name,
        issue_date=issue_date,
        appearance_change=appearance_change,
        max_speed_change=max_speed_change,
        power_change=power_change
    )
    db.add(db_change)
    db.commit()
    db.refresh(db_change)
    return db_change


@app.get("/changes/")
def read_changes(db: Session = Depends(get_db)):
    return db.query(Change).all()


@app.get("/changes/{change_id}")
def read_change(change_id: int, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")
    return db_change


@app.put("/changes/{change_id}")
def update_change(change_id: int, mechanic_name: str, issue_date: date, appearance_change: int, max_speed_change: int,
                  power_change: int, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    db_change.mechanic_name = mechanic_name
    db_change.issue_date = issue_date
    db_change.appearance_change = appearance_change
    db_change.max_speed_change = max_speed_change
    db_change.power_change = power_change

    db.commit()
    db.refresh(db_change)
    return db_change


@app.delete("/changes/{change_id}")
def delete_change(change_id: int, db: Session = Depends(get_db)):
    db_change = db.query(Change).filter(Change.issue_id == change_id).first()
    if db_change is None:
        raise HTTPException(status_code=404, detail="Change not found")

    db.delete(db_change)
    db.commit()
    return {"message": "Change deleted"}
