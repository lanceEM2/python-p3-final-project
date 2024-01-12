from seed import create_session, seed_data
from models import Showroom, Carowner, Car

def main():
    
    print("Welcome to the Showroom Database CLI!")

    session = create_session()

    while True:
        print("\nOptions:")
        print("1. Seed Data")
        print("2. Add Owner")
        print("3. Show Showroom Name and Location")
        print("4. Add Car to Owner")
        print("5. Delete Car from Owner")
        print("6. Show Cars with CC above 7000")
        print("7. Delete Owner")
        print("8. Exit")

        # Validates user input
        choice = input("Enter your choice: ")

        if choice == '1':
            seed_data(session)
            print("Data seeded successfully!")

        elif choice == '2':
            showroom_id = int(input("Enter Showroom ID: "))
            showroom = session.query(Showroom).get(showroom_id)
            if showroom:
                first_name = input("Enter Owner First Name: ")
                last_name = input("Enter Owner Last Name: ")
                new_owner = showroom.add_owner(first_name, last_name)
                session.add(new_owner)
                session.commit()
                print(f"Added new owner {new_owner.full_name()} in cars table.")
            else:
                print(f"No showroom found with ID {showroom_id}.")

        elif choice == '3':
            showroom_id = int(input("Enter Showroom ID: "))
            showroom = session.query(Showroom).get(showroom_id)
            if showroom:
                print(showroom.showroom_name())
            else:
                print(f"No showroom found with ID {showroom_id}.")

        elif choice == '4':
            owner_id = int(input("Enter Owner ID: "))     
            owner = session.query(Carowner).get(owner_id)
            if owner:
                car_name = input("Enter Car Name: ")
                car_cc = int(input("Enter Car CC: "))
                new_car = owner.add_car(car_name, car_cc)
                session.add(new_car)
                session.commit()
                print(f"Added new car {new_car} for owner {owner.full_name()}.")
            else:
                print(f"No owner found with ID {owner_id}.")

        elif choice == '5':
            owner_id = int(input("Enter Owner ID: "))
            owner = session.query(Carowner).get(owner_id)
            if owner:
                car_id = int(input("Enter Car ID to delete: "))
                result = owner.delete_car(session, car_id)
                session.commit()
                print(result)
            else:
                print(f"No owner found with ID {owner_id}.")

        elif choice == '6':
           high_cc_cars = Car.showcase_high_cc_cars(session)
           print("\nCars with CC above 7000:")
           for car in high_cc_cars:
               print(f"{car}")

        elif choice == '7':
            showroom_id = int(input("Enter Showroom ID: "))
            showroom = session.query(Showroom).get(showroom_id)
            if showroom:
                owner_id = int(input("Enter Owner ID to delete: "))
                result = showroom.delete_owner(session, owner_id)  # Pass the session to the delete_owner method
                session.commit()  # Make sure to commit the changes to the database
                print(result)
            else:
                print(f"No showroom found with ID {showroom_id}.")

        elif choice == '8':
            print("Exiting CLI. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == '__main__':
    main()