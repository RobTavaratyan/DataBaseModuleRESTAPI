from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from FastAPI.CRUD import get_db
from FastAPI.init_models import Car, Detail, Change

app = FastAPI()


@app.get("/cars/filter")
async def filter_cars(owner: str, brand: str, created_after: str, db: Session = Depends(get_db)):
    """
    SELECT brand, COUNT(*) as car_count FROM cars GROUP BY brand;

    GET /cars/filter?owner=John&brand=Toyota&created_after=2020-01-01
    """
    cars = db.query(Car).filter(
        Car.owner == owner,
        Car.brand == brand,
        Car.created_at > created_after
    ).all()
    return {"cars": cars}


@app.get("/cars/{car_id}/details")
async def get_car_details(car_id: int, db: Session = Depends(get_db)):
    """
    SELECT details.*
    FROM details
    JOIN changes ON details.id = changes.appearance_change
    WHERE changes.car_id = 1;

    GET /cars/1/details
    """
    details = db.query(Detail).join(Change, Detail.id == Change.appearance_change).filter(Change.car_id == car_id).all()
    return {"details": details}


@app.put("/cars/update_power")
async def update_power(brand: str, created_before: str, db: Session = Depends(get_db)):
    """
    UPDATE cars SET power = power * 1.2 WHERE brand = 'BMW' AND created_at < '2020-01-01';

    PUT /cars/update_power?brand=BMW&created_before=2020-01-01
    """
    db.query(Car).filter(
        Car.brand == brand,
        Car.created_at < created_before
    ).update({Car.power: Car.power * 1.2})
    db.commit()
    return {"message": "Power updated successfully"}


@app.get("/cars/group_by_brand")
async def group_by_brand(db: Session = Depends(get_db)):
    """
    SELECT brand, COUNT(*) as car_count FROM cars GROUP BY brand;

    GET /cars/group_by_brand
    """
    results = db.query(Car.brand, func.count(Car.id).label("car_count")).group_by(Car.brand).all()
    return {"brands": results}


@app.get("/cars/sort")
async def sort_cars(order_by: str = "power", direction: str = "desc", db: Session = Depends(get_db)):
    """
    SELECT * FROM cars ORDER BY power DESC;

    GET /cars/sort?order_by=power&direction=desc
    """
    if direction not in ["asc", "desc"]:
        direction = "asc"
    order_column = getattr(Car, order_by)
    if direction == "desc":
        order_column = desc(order_column)
    cars = db.query(Car).order_by(order_column).all()
    return {"cars": cars}
