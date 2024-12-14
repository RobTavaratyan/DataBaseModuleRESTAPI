import random
from datetime import datetime, timedelta, date
import requests
import time

# Define BASE_URL for your FastAPI server
BASE_URL = "http://localhost:8000"  # Change this to your FastAPI server URL


# Function to serialize date and datetime objects
def serialize_dates(data):
    if isinstance(data, datetime):
        return data.isoformat()  # Converts datetime to ISO format
    elif isinstance(data, date):
        return data.isoformat()  # Converts date to ISO format
    elif isinstance(data, dict):
        return {key: serialize_dates(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_dates(item) for item in data]
    return data  # Return other types as they are


# Function to generate car data
def generate_car_data():
    owners = ["John", "Alice", "Bob", "Charlie", "Eva"]
    brands = ["Toyota", "BMW", "Audi", "Mercedes", "Ford"]
    appearances = ["Sedan", "SUV", "Coupe", "Hatchback", "Convertible"]

    owner = random.choice(owners)
    brand = random.choice(brands)
    appearance = random.choice(appearances)
    power = random.randint(100, 400)
    max_speed = random.randint(180, 300)
    created_at = datetime.now() - timedelta(days=random.randint(0, 365))

    car_data = {
        "owner": owner,
        "brand": brand,
        "appearance": appearance,
        "power": power,
        "max_speed": max_speed,
        "created_at": created_at.date(),  # Use date (ensure it's in 'YYYY-MM-DD' format)
    }

    # Serialize the dates before sending the request
    return serialize_dates(car_data)


# Function to generate detail data
def generate_detail_data():
    names = ["Brake Pads", "Engine Oil", "Alternator", "Battery", "Tire"]
    car_parts = ["Front", "Rear", "Left", "Right"]
    firms = ["Bosch", "Magneti Marelli", "SKF", "Valeo", "Delphi"]

    name = random.choice(names)
    car_part = random.choice(car_parts)
    firm = random.choice(firms)
    price = random.uniform(20.0, 500.0)  # Random price
    guarantee = datetime.now() + timedelta(
        days=random.randint(365, 1825)
    )  # Guarantee from 1 to 5 years

    detail_data = {
        "name": name,
        "car_part": car_part,
        "firm": firm,
        "price": price,
        "guarantee": guarantee.date(),  # Use date for guarantee
    }

    # Serialize the dates before sending the request
    return serialize_dates(detail_data)


# Function to generate change data
def generate_change_data(
    car_id, appearance_detail_id, max_speed_detail_id, power_detail_id
):
    mechanic_names = ["John", "Sam", "Tina", "Paul", "Rita"]

    mechanic_name = random.choice(mechanic_names)
    issue_date = datetime.now() - timedelta(days=random.randint(0, 365))

    change_data = {
        "car_id": car_id,
        "mechanic_name": mechanic_name,
        "issue_date": issue_date.date(),  # Use date for issue_date
        "appearance_change": appearance_detail_id,
        "max_speed_change": max_speed_detail_id,
        "power_change": power_detail_id,
    }

    # Serialize the dates before sending the request
    return serialize_dates(change_data)


# Function to add cars
def add_cars(num_cars):
    for _ in range(num_cars):
        car_data = generate_car_data()

        print(car_data)

        response = requests.post(f"{BASE_URL}/cars/", json=car_data)
        if response.status_code == 200:
            print(f"Car added: {car_data}")
        else:
            print(f"Failed to add car: {response.status_code} - {response.text}")

        time.sleep(0.1)  # Sleep for 100ms to avoid overwhelming the server


# Function to add details
def add_details(num_details):
    for _ in range(num_details):
        detail_data = generate_detail_data()
        response = requests.post(f"{BASE_URL}/details/", json=detail_data)
        if response.status_code == 200:
            print(f"Detail added: {detail_data}")
        else:
            print(f"Failed to add detail: {response.status_code}")

        time.sleep(0.1)  # Sleep for 100ms to avoid overwhelming the server


# Function to add changes
def add_changes(num_changes, num_cars, num_details):
    for _ in range(num_changes):
        car_id = random.randint(1, num_cars)
        appearance_detail_id = random.randint(1, num_details)
        max_speed_detail_id = random.randint(1, num_details)
        power_detail_id = random.randint(1, num_details)

        change_data = generate_change_data(
            car_id, appearance_detail_id, max_speed_detail_id, power_detail_id
        )

        # Print change_data to verify it's structured properly
        print(change_data)

        response = requests.post(f"{BASE_URL}/changes/", json=change_data)
        if response.status_code == 200:
            print(f"Change added: {change_data}")
        else:
            print(f"Failed to add change: {response.status_code} - {response.text}")

        time.sleep(0.1)  # Sleep for 100ms to avoid overwhelming the server


# Number of cars, details, and changes to generate
NUM_CARS = 100
NUM_DETAILS = 50
NUM_CHANGES = 100

add_cars(NUM_CARS)
add_details(NUM_DETAILS)
add_changes(NUM_CHANGES, NUM_CARS, NUM_DETAILS)
