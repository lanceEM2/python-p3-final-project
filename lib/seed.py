#!/usr/bin/env python3

import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Showroom, Carowner, Car

fake = Faker()

car_brands = ["Toyota", "Ford", "Honda", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", "Volkswagen", "Audi", "Tesla",
                "Subaru", "Hyundai", "Kia", "Lexus", "Porsche", "Jaguar", "Land Rover", "Ferrari", "Maserati", "Volvo"
            ]

litre_cc = [1000, 1500, 1800, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]

companies = ["Rift Cars", "CarNation", "Kai and Karo", "Mascardi"]

def create_session():
    engine = create_engine('sqlite:///showroom.db')
    Session = sessionmaker(bind=engine)
    return Session()

def generate_random_showroom(index):
    return Showroom(
        name = companies[index - 1],
        location = fake.city()
    )

def generate_random_carowner(showroom):
    return Carowner(
        first_name = fake.first_name(),
        last_name = fake.last_name(),
        showroom = showroom
    )

def generate_random_car(showroom, carowner):
    return Car(
        car_name = random.choice(car_brands),
        car_cc = random.choice(litre_cc),
        showroom = showroom,
        owner = carowner
    )

def seed_data(session, num_showrooms = 4, num_carowners = 20, num_cars = 20):
    showrooms = [generate_random_showroom(i) for i in range(1, num_showrooms + 1)]
    session.add_all(showrooms)
    session.flush()

    carowners = [
        generate_random_carowner(random.choice(showrooms)) for _ in range(num_carowners)
    ]
    session.add_all(carowners)
    session.flush()

    cars = [
        generate_random_car(random.choice(showrooms), random.choice(carowners))
        for _ in range(num_cars)
    ]
    session.add_all(cars)
    session.flush()

    session.commit()

if __name__ == '__main__':
    session = create_session()
    
    session.query(Showroom).delete()
    session.query(Carowner).delete()
    session.query(Car).delete()

    seed_data(session)