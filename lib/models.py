from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///showroom.db')

Base = declarative_base()

class Showroom(Base):
    __tablename__ = 'showrooms'

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    location = Column(String())

    # Showroom has one-to-many relationship with cars table
    cars = relationship('Car', back_populates= 'showroom')
    # Showroom has one-to-many relationship with carowners table
    carowners = relationship('Carowner', back_populates= 'showroom')

    # returns all instances of cars
    def all_cars(self):
        return self.cars

    # add a car owner to the carowners table
    def add_owner(self, first_name, last_name):
        new_owner = Carowner(first_name = first_name, last_name = last_name, showroom = self)
        self.carowners.append(new_owner)
        return new_owner

    # deletes an owner in carowners table
    def delete_owner(self, session, owner_id):
        owner_to_delete = next((owner for owner in self.carowners if owner.id == owner_id), None)
        if owner_to_delete:
            self.carowners.remove(owner_to_delete)
            session.delete(owner_to_delete)  # Deletes the owner from the database
            return f"Deleted owner with ID {owner_id} from {self.showroom_name()}"
        else:
            return f"No owner found with ID {owner_id} in {self.showroom_name()}"

    def showroom_name(self):
        return f"Showroom Name: {self.name}, Location: {self.location}"

class Carowner(Base):
    __tablename__ = 'carowners'

    id = Column(Integer(), primary_key = True)
    first_name = Column(String())
    last_name = Column(String())

    # Carowner has one-to-many relationship with cars table
    cars = relationship('Car', back_populates= 'owner')
    # A showroom can have multiple car owners, but each car owner is associated with only one showroom (many-to-one relationship).
    showroom = relationship('Showroom', back_populates= 'carowners')

    showroom_id = Column(Integer(), ForeignKey('showrooms.id'))

    # returns the full name of the car owner
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # adds a car in the cars table
    def add_car(self, car_name, car_cc):
        new_car = Car(car_name = car_name, car_cc = car_cc, showroom = self.showroom, owner = self)
        self.cars.append(new_car)
        return new_car

    # deletes a car in cars table
    def delete_car(self, session, car_id):
        car_to_delete = next((car for car in self.cars if car.id == car_id), None)
        if car_to_delete:
            self.cars.remove(car_to_delete)
            session.delete(car_to_delete) # Deletes the car from the database
            return f"Deleted car with ID {car_id} for {self.full_name()}"
        else:
            return f"No car found with ID {car_id} for {self.full_name()}"

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer(), primary_key = True)
    car_name = Column(String())
    car_cc = Column(Integer())

    # Car has many-to-one relationship with showroom (many cars can belong to one showroom)
    showroom_id = Column(Integer(), ForeignKey('showrooms.id'))
    # Car has many-to-one relationship with car owner (many cars can belong to one owner)
    owner_id = Column(Integer(), ForeignKey('carowners.id'))

    showroom = relationship('Showroom', back_populates= 'cars')
    owner = relationship('Carowner', back_populates= 'cars')

    def __repr__(self):
        return f"<Car(id={self.id}, car_name={self.car_name}, car_cc={self.car_cc})>"

    @classmethod
    def showcase_high_cc_cars(cls, session):
        high_cc_cars = session.query(cls).filter(cls.car_cc > 7000).all()
        return high_cc_cars