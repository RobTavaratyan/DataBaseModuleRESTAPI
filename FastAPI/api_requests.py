import requests
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from datetime import date

from FastAPI.router import get_db
from alchemy.init_models import Car, Detail, Change
from FastAPI.main import fastapi_app as app


@app.get("/cars/filter")
async def filter_cars(
        owner: str,
        brand: str,
        created_after: str,
        order_by: str = "created_at",
        direction: str = "desc",
        db: Session = Depends(get_db),
):
    """
    SELECT * FROM cars WHERE owner = :owner AND brand = :brand AND created_at > :created_after;

    GET /cars/filter?owner=John&brand=Toyota&created_after=2020-01-01&order_by=created_at&direction=asc
    """
    # Convert created_after to a date object
    try:
        created_after_date = date.fromisoformat(
            created_after
        )  # Assumes the format is 'YYYY-MM-DD'
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'."
        )

    cars_query = db.query(Car).filter(
        Car.owner == owner, Car.brand == brand, Car.created_at > created_after_date
    )

    # Sorting logic
    if direction not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid direction. Use 'asc' or 'desc'."
        )

    order_column = getattr(Car, order_by, None)
    if order_column is None:
        raise HTTPException(status_code=400, detail="Invalid column to order by.")

    if direction == "desc":
        cars_query = cars_query.order_by(desc(order_column))
    else:
        cars_query = cars_query.order_by(asc(order_column))

    cars = cars_query.all()
    if not cars:
        raise HTTPException(
            status_code=404, detail="No cars found with the given criteria."
        )

    return {"cars": cars}


@app.get("/cars/{car_id}/details")
async def get_car_details(
        car_id: int,
        order_by: str = "id",
        direction: str = "asc",
        db: Session = Depends(get_db),
):
    """
    SELECT details.* FROM details
    JOIN changes ON details.id = changes.appearance_change
    WHERE changes.car_id = :car_id;

    GET /cars/1/details?order_by=price&direction=desc
    """
    if direction not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid direction. Use 'asc' or 'desc'."
        )

    details_query = (
        db.query(Detail)
        .join(Change, Detail.id == Change.appearance_change)
        .filter(Change.car_id == car_id)
    )

    # Sorting logic
    order_column = getattr(Detail, order_by, None)
    if order_column is None:
        raise HTTPException(status_code=400, detail="Invalid column to order by.")

    if direction == "desc":
        details_query = details_query.order_by(desc(order_column))
    else:
        details_query = details_query.order_by(asc(order_column))

    details = details_query.all()
    if not details:
        raise HTTPException(status_code=404, detail="No details found for this car.")

    return {"details": details}


@app.put("/cars/update_power")
async def update_power(brand: str, created_before: str, db: Session = Depends(get_db)):
    """
    UPDATE cars SET power = power * 1.2
    WHERE brand = :brand AND created_at < :created_before;

    PUT /cars/update_power?brand=BMW&created_before=2020-01-01
    """
    # Convert created_before to a date object
    try:
        created_before_date = date.fromisoformat(
            created_before
        )  # Assumes the format is 'YYYY-MM-DD'
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'."
        )

    cars_to_update = db.query(Car).filter(
        Car.brand == brand, Car.created_at < created_before_date
    )

    updated_count = cars_to_update.update(
        {Car.power: Car.power * 1.2}, synchronize_session=False
    )
    db.commit()

    if updated_count == 0:
        raise HTTPException(
            status_code=404, detail="No cars found with the given criteria to update."
        )

    return {"message": f"{updated_count} car(s) power updated successfully."}


@app.get("/cars/group_by_brand")
async def group_by_brand(
        order_by: str = "brand", direction: str = "asc", db: Session = Depends(get_db)
):
    """
    SELECT brand, COUNT(*) as car_count FROM cars GROUP BY brand;

    GET /cars/group_by_brand?order_by=car_count&direction=desc
    """
    if direction not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid direction. Use 'asc' or 'desc'."
        )

    results_query = db.query(Car.brand, func.count(Car.id).label("car_count")).group_by(
        Car.brand
    )

    # Sorting logic
    if order_by == "car_count":
        results_query = results_query.order_by(
            desc("car_count") if direction == "desc" else asc("car_count")
        )
    else:
        order_column = getattr(Car, order_by, None)
        if order_column is None:
            raise HTTPException(status_code=400, detail="Invalid column to order by.")
        if direction == "desc":
            results_query = results_query.order_by(desc(order_column))
        else:
            results_query = results_query.order_by(asc(order_column))

    results = results_query.all()
    return {"brands": results}


@app.get("/cars/sort")
async def sort_cars(
        order_by: str = "power", direction: str = "desc", db: Session = Depends(get_db)
):
    """
    SELECT * FROM cars ORDER BY :order_by :direction;

    GET /cars/sort?order_by=power&direction=desc
    """
    if direction not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail="Invalid direction. Use 'asc' or 'desc'."
        )

    order_column = getattr(Car, order_by, None)
    if order_column is None:
        raise HTTPException(status_code=400, detail="Invalid column to sort by.")

    cars_query = db.query(Car).order_by(
        desc(order_column) if direction == "desc" else asc(order_column)
    )
    cars = cars_query.all()
    return {"cars": cars}

res = requests.get('http://127.0.0.1:8000/cars/filter?owner=John&brand=Toyota&created_after=2020-01-01&order_by=created_at&direction=asc')
print(res.json())


"""
curl -X 'GET' \
  'http://127.0.0.1:8000/cars/filter?owner=John&brand=Toyota&created_after=2020-01-01&order_by=created_at&direction=asc'

curl -X 'GET' \
  'http://127.0.0.1:8000/cars/1/details?order_by=id&direction=desc'

curl -X 'PUT' \
  'http://127.0.0.1:8000/cars/update_power?brand=BMW&created_before=2020-01-01'

curl -X 'GET' \
  'http://127.0.0.1:8000/cars/group_by_brand?order_by=car_count&direction=desc'

curl -X 'GET' \
  'http://127.0.0.1:8000/cars/sort?order_by=power&direction=desc'


"""
