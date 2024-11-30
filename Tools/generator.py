import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"


def generate_car_data():
    owners = ["Alice", "Bob", "Charlie", "David", "Eva"]
    brands = ["Toyota", "BMW", "Audi", "Mercedes", "Ford"]
    appearances = ["Sedan", "SUV", "Coupe", "Hatchback", "Convertible"]

    owner = random.choice(owners)
    brand = random.choice(brands)
    appearance = random.choice(appearances)
    power = random.randint(100, 400)
    max_speed = random.randint(180, 300)
    created_at = datetime.now() - timedelta(days=random.randint(0, 365))

    return {
        "owner": owner,
        "brand": brand,
        "appearance": appearance,
        "power": power,
        "max_speed": max_speed,
        "created_at": created_at.date()
    }


def generate_detail_data():
    names = ["Brake Pads", "Engine Oil", "Alternator", "Battery", "Tire"]
    car_parts = ["Front", "Rear", "Left", "Right"]
    firms = ["Bosch", "Magneti Marelli", "SKF", "Valeo", "Delphi"]

    name = random.choice(names)
    car_part = random.choice(car_parts)
    firm = random.choice(firms)
    price = random.uniform(20.0, 500.0)  # случайная цена
    guarantee = datetime.now() + timedelta(days=random.randint(365, 1825))  # гарантия от 1 до 5 лет

    return {
        "name": name,
        "car_part": car_part,
        "firm": firm,
        "price": price,
        "guarantee": guarantee.date()
    }


def generate_change_data(car_id, appearance_detail_id, max_speed_detail_id, power_detail_id):
    mechanic_names = ["John", "Sam", "Tina", "Paul", "Rita"]

    mechanic_name = random.choice(mechanic_names)
    issue_date = datetime.now() - timedelta(days=random.randint(0, 365))

    return {
        "car_id": car_id,
        "mechanic_name": mechanic_name,
        "issue_date": issue_date.date(),
        "appearance_change": appearance_detail_id,
        "max_speed_change": max_speed_detail_id,
        "power_change": power_detail_id
    }


def add_cars(num_cars):
    for _ in range(num_cars):
        car_data = generate_car_data()
        response = requests.post(f"{BASE_URL}/cars/", json=car_data)
        if response.status_code == 200:
            print(f"Car added: {car_data}")
        else:
            print(f"Failed to add car: {response.status_code}")


def add_details(num_details):
    for _ in range(num_details):
        detail_data = generate_detail_data()
        response = requests.post(f"{BASE_URL}/details/", json=detail_data)
        if response.status_code == 200:
            print(f"Detail added: {detail_data}")
        else:
            print(f"Failed to add detail: {response.status_code}")


def add_changes(num_changes, num_cars, num_details):
    for _ in range(num_changes):
        car_id = random.randint(1, num_cars)
        appearance_detail_id = random.randint(1, num_details)
        max_speed_detail_id = random.randint(1, num_details)
        power_detail_id = random.randint(1, num_details)

        change_data = generate_change_data(car_id, appearance_detail_id, max_speed_detail_id, power_detail_id)
        response = requests.post(f"{BASE_URL}/changes/", json=change_data)
        if response.status_code == 200:
            print(f"Change added: {change_data}")
        else:
            print(f"Failed to add change: {response.status_code}")


NUM_CARS = 10000
NUM_DETAILS = 5000
NUM_CHANGES = 10000
add_cars(NUM_CARS)
add_details(NUM_DETAILS)
add_changes(NUM_CHANGES, NUM_CARS, NUM_DETAILS)
