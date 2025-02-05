# Importing necessary packages to run application and setting up connection to database
# Random used to generate random duration of new flight routes

import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect('flight_management_system.db')
cursor = conn.cursor()

# Deleting any tables that may already exist prior re-initialising db and testing app

cursor.execute("DROP TABLE IF EXISTS Countries")
cursor.execute("DROP TABLE IF EXISTS Cities")
cursor.execute("DROP TABLE IF EXISTS Airports")
cursor.execute("DROP TABLE IF EXISTS Pilots")
cursor.execute("DROP TABLE IF EXISTS Routes")
cursor.execute("DROP TABLE IF EXISTS Flights")

# Creating database tables. Structure designed to adhere to the rules of 3NF.

cursor.execute(
    'CREATE TABLE Countries (country_ID INTEGER PRIMARY KEY AUTOINCREMENT, country_name TEXT NOT NULL UNIQUE);'
)

cursor.execute(
    'CREATE TABLE Cities (city_ID INTEGER PRIMARY KEY AUTOINCREMENT, city_name TEXT NOT NULL, country_ID INTEGER NOT NULL, FOREIGN KEY (country_ID) REFERENCES Countries(country_ID), UNIQUE(city_name, country_ID));'
)

cursor.execute(
    'CREATE TABLE Airports (airport_ID TEXT NOT NULL PRIMARY KEY, airport_name TEXT NOT NULL, city_ID INTEGER NOT NULL, FOREIGN KEY (city_ID) REFERENCES Cities(city_ID));'
)

cursor.execute(
    'CREATE TABLE Pilots (pilot_ID INTEGER PRIMARY KEY, pilot_name TEXT NOT NULL, nationality_country_ID INTEGER NOT NULL, pilot_age INTEGER NOT NULL, FOREIGN KEY (nationality_country_ID) REFERENCES Countries(country_ID), CHECK (pilot_age >= 18 AND pilot_age <= 65));'
)

cursor.execute(
    'CREATE TABLE Routes (route_ID INTEGER PRIMARY KEY, departure_airport TEXT NOT NULL, arrival_airport TEXT NOT NULL, duration INTEGER NOT NULL, FOREIGN KEY (departure_airport) REFERENCES Airports(airport_ID), FOREIGN KEY (arrival_airport) REFERENCES Airports(airport_ID), UNIQUE (departure_airport, arrival_airport), CHECK (departure_airport != arrival_airport));'
)

cursor.execute(
    'CREATE TABLE Flights (flight_ID INTEGER PRIMARY KEY, pilot_ID INTEGER NOT NULL, route_ID INTEGER NOT NULL, departure_datetime DATETIME NOT NULL, FOREIGN KEY (pilot_ID) REFERENCES Pilots(pilot_ID), FOREIGN KEY (route_ID) REFERENCES Routes(route_ID));'
)

# Populating tables with data

cursor.execute(
    "INSERT INTO Countries (country_name) VALUES ('England'), ('Northern Ireland'), ('Scotland'), ('France'), ('Netherlands'), ('Portugal'), ('Spain'), ('Germany'), ('Italy')"
)

cursor.execute(
    "INSERT INTO Cities (city_name, country_ID) VALUES ('London', 1), ('Bristol', 1), ('Belfast', 2), ('Edinburgh', 3), ('Birmingham', 1), ('Manchester', 1), ('Paris', 4), ('Amsterdam', 5), ('Porto', 6), ('Madrid', 7), ('Berlin', 8), ('Rome', 9)"
)

cursor.execute(
    "INSERT INTO Airports (airport_ID, airport_name, city_ID) VALUES \
  ('LHR', 'London Heathrow Airport', 1), \
  ('BRS', 'Bristol Airport', 2), \
  ('LGW', 'London Gatwick Airport', 1), \
  ('BFS', 'Aldergrove International Airport', 3), \
  ('EDI', 'Edinburgh Airport', 4), \
  ('BHX', 'Birmingham Airport', 5), \
  ('MAN', 'Manchester Airport', 6), \
  ('CDG', 'Paris Charles de Gaulle Airport', 7), \
  ('AMS', 'Amsterdam Airport Schiphol', 8), \
  ('OPO', 'Porto Airport', 9), \
  ('MAD', 'Madrid Barajas Airport', 10), \
  ('BER', 'Berlin Brandenburg Airport', 11), \
  ('FCO', 'Leonardo da Vinci-Fiumicino Airport', 12)")

cursor.execute(
    "INSERT INTO Pilots (pilot_ID, pilot_name, nationality_country_ID, pilot_age) VALUES \
  (1, 'James Smith', 'England', 30), \
  (2, 'Michael Johnson', 'England', 35), \
  (3, 'Emily Davis', 'England', 28), \
  (4, 'David Wilson', 'England', 42), \
  (5, 'Sophia Taylor', 'England', 25), \
  (6, 'William Brown', 'England', 40), \
  (7, 'Olivia Thomas', 'England', 33), \
  (8, 'Joseph Anderson', 'England', 31), \
  (9, 'Ava Martinez', 'Spain', 49), \
  (10, 'Daniel Clark', 'England', 37)")

cursor.execute(
    "INSERT INTO Routes (route_ID, departure_airport, arrival_airport, duration) VALUES \
  (1, 'LHR', 'BFS', 85), \
  (2, 'LHR', 'EDI', 85), \
  (3, 'LHR', 'CDG', 80), \
  (4, 'LHR', 'AMS', 75), \
  (5, 'LHR', 'MAD', 150), \
  (6, 'LHR', 'BER', 115), \
  (7, 'LHR', 'FCO', 155), \
  (8, 'CDG', 'MAD', 125), \
  (9, 'CDG', 'FCO', 120), \
  (10, 'AMS', 'BER', 95), \
  (11, 'AMS', 'CDG', 75), \
  (12, 'MAD', 'FCO', 145), \
  (13, 'BER', 'FCO', 120), \
  (14, 'EDI', 'AMS', 105), \
  (15, 'EDI', 'CDG', 115), \
  (16, 'BFS', 'AMS', 110), \
  (17, 'BFS', 'CDG', 120), \
  (18, 'BRS', 'AMS', 105), \
  (19, 'BRS', 'CDG', 100), \
  (20, 'BRS', 'MAD', 135), \
  (21, 'LGW', 'CDG', 80), \
  (22, 'LGW', 'AMS', 75), \
  (23, 'LGW', 'MAD', 145), \
  (24, 'BHX', 'CDG', 95), \
  (25, 'BHX', 'AMS', 90), \
  (26, 'MAN', 'CDG', 100), \
  (27, 'MAN', 'AMS', 95), \
  (28, 'MAN', 'MAD', 155), \
  (29, 'CDG', 'BER', 110), \
  (30, 'MAD', 'BER', 165), \
  (31, 'BFS', 'LHR', 85), \
  (32, 'EDI', 'LHR', 85), \
  (33, 'CDG', 'LHR', 80), \
  (34, 'AMS', 'LHR', 75), \
  (35, 'MAD', 'LHR', 150), \
  (36, 'BER', 'LHR', 115), \
  (37, 'FCO', 'LHR', 155), \
  (38, 'MAD', 'CDG', 125), \
  (39, 'FCO', 'CDG', 120), \
  (40, 'BER', 'AMS', 95), \
  (41, 'CDG', 'AMS', 75), \
  (42, 'FCO', 'MAD', 145), \
  (43, 'FCO', 'BER', 120), \
  (44, 'AMS', 'EDI', 105), \
  (45, 'CDG', 'EDI', 115), \
  (46, 'AMS', 'BFS', 110), \
  (47, 'CDG', 'BFS', 120), \
  (48, 'AMS', 'BRS', 105), \
  (49, 'CDG', 'BRS', 100), \
  (50, 'MAD', 'BRS', 135), \
  (51, 'CDG', 'LGW', 80), \
  (52, 'AMS', 'LGW', 75), \
  (53, 'MAD', 'LGW', 145), \
  (54, 'CDG', 'BHX', 95), \
  (55, 'AMS', 'BHX', 90), \
  (56, 'CDG', 'MAN', 100), \
  (57, 'AMS', 'MAN', 95), \
  (58, 'MAD', 'MAN', 155), \
  (59, 'BER', 'CDG', 110), \
  (60, 'BER', 'MAD', 165)")

cursor.execute(
    """INSERT INTO Flights (flight_ID, pilot_ID, route_ID, departure_datetime) VALUES 
  (100001, 1, 1, datetime('now', 'start of day', '+8 hours', '+30 minutes')),
  (100002, 2, 3, datetime('now', 'start of day', '+9 hours', '+15 minutes')),
  (100003, 3, 5, datetime('now', 'start of day', '+10 hours')),
  (100004, 4, 7, datetime('now', 'start of day', '+11 hours', '+30 minutes')),
  (100005, 5, 2, datetime('now', '+1 day', 'start of day', '+7 hours', '+45 minutes')),
  (100006, 6, 4, datetime('now', '+2 days', 'start of day', '+8 hours', '+30 minutes')),
  (100007, 7, 6, datetime('now', '+3 days', 'start of day', '+9 hours', '+45 minutes')),
  (100008, 8, 8, datetime('now', '+4 days', 'start of day', '+14 hours', '+15 minutes')),
  (100009, 9, 10, datetime('now', '+5 days', 'start of day', '+6 hours', '+30 minutes')),
  (100010, 10, 12, datetime('now', '+6 days', 'start of day', '+7 hours', '+45 minutes')),
  (100011, 1, 14, datetime('now', '+7 days', 'start of day', '+8 hours', '+15 minutes'))"""
)


# Functions for carrying out CRUD operations on data:

# ADD FLIGHT FUNCTION

def add_flight():
    print("\nAdd New Flight:")
    # Show available departure airports (i.e. all airports)
    cursor.execute("SELECT * FROM Airports")
    airports = cursor.fetchall()
    print("\nAvailable departure airports:")
    for airport in airports:
        # Print airport_ID and airport_name
        print("{}: {}".format(airport[0], airport[1]))

    # Ask user for their choice of departure airport
    departure_airport = input("\nEnter departure airport code (e.g. LHR): ")

    # Show available arrival airports for selected departure airport
    cursor.execute(
        """
        SELECT DISTINCT Airports.airport_ID, Airports.airport_name 
        FROM Airports 
        INNER JOIN Routes ON Airports.airport_ID = Routes.arrival_airport 
        WHERE Routes.departure_airport = ?""", (departure_airport,))
    arrival_airports = cursor.fetchall()

    print("\nAvailable arrival airports:")
    for airport in arrival_airports:
        print("{}: {}".format(airport[0], airport[1]))

    # Ask user for their choice of arrival airport (no case sensitivity)
    arrival_airport = input("\nEnter arrival airport code (e.g. LHR): ").upper()

    # Make sure user input is in the list of available arrival airports
    if arrival_airport not in [airport[0] for airport in arrival_airports]:
        print(
            "{} is not a valid option. Please try again.".format(arrival_airport))
        return

    # Ask user for flight time
    departure_datetime = input("Enter departure datetime (YYYY-MM-DD HH:MM): ")

    # Make sure date/time in correct format
    try:
        datetime.strptime(departure_datetime, '%Y-%m-%d %H:%M')
    except (IndexError, ValueError):
        print("Invalid date format. Please use YYYY-MM-DD HH:MM")
        return

    # Ask user for selected pilot_ID
    pilot_id = input("Enter pilot ID: ")

    # Check if pilot_ID exists
    cursor.execute("SELECT * FROM Pilots WHERE pilot_ID = ?", (pilot_id,))
    pilot = cursor.fetchone()
    if not pilot:
        print("Pilot {} does not exist. Please enter a valid pilot ID.".format(
            pilot_id))
        return

    # Get pilot's last flight to determine current location
    # Pilot's filtered flights organised in descending order by departure_datetime, then top flight is selected to determine current location
    cursor.execute(
        "SELECT Routes.arrival_airport FROM Flights JOIN Routes ON Flights.route_ID = Routes.route_ID WHERE Flights.pilot_ID = ? AND Flights.departure_datetime < ? ORDER BY Flights.departure_datetime DESC",
        (pilot_id, departure_datetime))
    last_location = cursor.fetchone()

    # If no previous flights, assume pilot is at departure airport
    current_location = last_location[0] if last_location else departure_airport

    # Get route details and validate pilot location
    cursor.execute(
        "SELECT Routes.route_ID FROM Routes WHERE Routes.departure_airport = ? AND Routes.arrival_airport = ?",
        (departure_airport, arrival_airport))
    route = cursor.fetchone()

    if current_location != departure_airport:
        print("Pilot {} is/will be in {} and cannot depart from {}".format(
            pilot_id, current_location, departure_airport))
        return

    # Add flight to database if no issues
    cursor.execute(
        "INSERT INTO Flights (pilot_ID, route_ID, departure_datetime) VALUES (?, ?, ?)",
        (pilot_id, route[0], departure_datetime))
    print("Flight added successfully.")


# ADD PILOT FUNCTION

def add_pilot():
    # Ask user to input pilot details
    # ValueError if pilot_age is integer but not in range (18-65)
    print("\nAdd New Pilot:")
    pilot_name = input("Enter pilot name: ")

    # Show available countries
    cursor.execute("SELECT country_ID, country_name FROM Countries")
    countries = cursor.fetchall()
    print("\nAvailable countries:")
    for country in countries:
        print(f"{country[0]}: {country[1]}")

    nationality_country_id = input("Enter nationality country ID: ")
    while True:
        try:
            pilot_age = int(input("Enter pilot age: "))
            if pilot_age < 18:
                print("Pilot must be 18 or older to be added to the system.")
                continue
            elif pilot_age > 65:
                print("Pilot must be 65 or younger to be added to the system.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Assign new pilot_id (+1 incremental integer assignment)
    cursor.execute("SELECT MAX(pilot_ID) FROM Pilots")
    max_pilot_id = cursor.fetchone()[0]
    pilot_id = max_pilot_id + 1 if max_pilot_id is not None else 1

    # Update database with new pilot
    cursor.execute(
        "INSERT INTO Pilots (pilot_ID, pilot_name, nationality_country_ID, pilot_age) VALUES (?, ?, ?, ?)",
        (pilot_id, pilot_name, nationality_country_id, pilot_age))
    print("Pilot {} added successfully.".format(pilot_name))


# ADD AIRPORT FUNCTION

def add_airport():
    # Ask user to input airport details
    print("\nAdd New Airport:")
    airport_ID = input("Enter airport code (e.g. LHR): ").upper()
    airport_name = input("Enter airport name: ")

    # Show available cities and their countries
    cursor.execute("""
    SELECT Cities.city_ID, Cities.city_name, Countries.country_name 
    FROM Cities 
    JOIN Countries ON Cities.country_ID = Countries.country_ID
    ORDER BY Countries.country_name, Cities.city_name
  """)
    cities = cursor.fetchall()
    print("\nAvailable cities:")
    for city in cities:
        print("{}: {} ({})".format(city[0], city[1], city[2]))

    city_id = input("\nEnter city ID: ")

    # Check if airport already exists in database
    cursor.execute("SELECT * FROM Airports WHERE airport_ID = ?", (airport_ID,))
    airport = cursor.fetchone()
    if airport:
        print("Airport {} already exists in the database.".format(airport_ID))
    else:
        # Insert new airport into database
        cursor.execute(
            "INSERT INTO Airports (airport_ID, airport_name, city_ID) VALUES (?, ?, ?)",
            (airport_ID, airport_name, city_id))
        print("Airport {} added successfully.".format(airport_name))


# ADD ROUTE FUNCTION

def add_route():
    # Ask user to input route details
    print("\nAdd New Route:")
    departure_airport = input("Enter departure airport code (e.g. LHR): ").upper()
    arrival_airport = input("Enter arrival airport code (e.g. LHR): ").upper()

    # Check if route already exists in database
    cursor.execute(
        "SELECT * FROM Routes WHERE departure_airport = ? AND arrival_airport = ?",
        (departure_airport, arrival_airport))
    route = cursor.fetchone()
    if route:
        print("Route from {} to {} already exists in the database.".format(
            departure_airport, arrival_airport))
        return

    # Add new route with incremental route_ID, selected airports, and random duration between 60 and 300 minutes (because don't have database for duration of routes between new airports)
    cursor.execute("SELECT MAX(route_ID) FROM Routes")
    max_route_ID = cursor.fetchone()[0]
    route_ID = max_route_ID + 1 if max_route_ID is not None else 1
    cursor.execute(
        "INSERT INTO Routes (route_ID, departure_airport, arrival_airport, duration) VALUES (?, ?, ?, ?)",
        (route_ID, departure_airport, arrival_airport, random.randint(60, 300)))
    print("Route between {} and {} added successfully.".format(
        departure_airport, arrival_airport))


# VIEW FLIGHTS FUNCTION

def view_flights():
    print("\n1. View All Flights")
    print("2. View Flights by Date")
    print("3. View Flights by Pilot")
    print("4. View Flights by Departure Location")
    print("5. View Flights by Destination")
    print("6. View Flights by Route")
    print("7. Return to Main Menu")
    choice = input("\nEnter your choice (1-7): ")
    if choice == "1":
        cursor.execute("""
      SELECT * FROM Flights
      JOIN Pilots ON Flights.pilot_ID = Pilots.pilot_ID
      JOIN Routes ON Flights.route_ID = Routes.route_ID
      ORDER BY Flights.departure_datetime
    """)
        flights = cursor.fetchall()
        print("\nAll Flights:")
        print("\nFlight ID | Pilot | From | To | Departure Time | Duration (mins)")
        print("-" * 65)
        for flight in flights:
            print("{:^9} | {:15} | {:<4} | {:<4} | {:14} | {:^8}".format(
                flight[0], flight[1], flight[2], flight[3], flight[4], flight[5]))

    elif choice == "2":
        # Get user to enter date
        date = input("Enter date (YYYY-MM-DD): ")
        cursor.execute("SELECT * FROM Flights WHERE departure_datetime = ?",
                       (date,))
        flights = cursor.fetchall()
        print("\nFlights on {}:".format(date))
        for flight in flights:
            print(flight)

    elif choice == "3":
        # Display pilot_ID and names
        cursor.execute("SELECT pilot_ID, pilot_name FROM Pilots")
        pilots = cursor.fetchall()
        print("\nPilots:")
        for pilot in pilots:
            print(pilot)
        # Ask user to input ID of pilot whose flights they wish to see
        pilot_id = input(
            "\nEnter the ID of the pilot whose flights you would like to view: ")
        # Display flights for that pilot by date.
        cursor.execute(
            "SELECT * FROM Flights WHERE pilot_ID = ? ORDER BY departure_datetime DESC",
            (pilot_id,))
        flights = cursor.fetchall()
        print(f"\nFlights for pilot {pilot_id}:")
        for flight in flights:
            print(flight)

    elif choice == "4":
        # Display airport_IDs and names
        cursor.execute("SELECT airport_ID, airport_name FROM Airports")
        airports = cursor.fetchall()
        print("\nAirports:")
        for airport in airports:
            print(airport)
        # Ask user to input ID of airport whose flights they wish to see
        airport_id = input(
            "\nEnter the ID of the airport whose flights you would like to view (e.g. LHR): "
        )
        # Display flights for that airport by date
        cursor.execute("SELECT * FROM Flights WHERE arrival_airport = ?",
                       (airport_id,))
        flights = cursor.fetchall()
        print("\nFlights for airport {}:".format(airport_id))
        for flight in flights:
            print(flight)

    elif choice == "5":
        # Display airport_IDs and names
        cursor.execute("SELECT airport_ID, airport_name FROM Airports")
        airports = cursor.fetchall()
        print("\nAirports:")
        for airport in airports:
            print(airport)
        # Ask user to input ID of airport whose flights they wish to see
        airport_id = input(
            "\nEnter the ID of the airport whose flights you would like to view (e.g. LHR): "
        ).upper()
        # Display flights for that airport by date
        cursor.execute("SELECT * FROM Flights WHERE departure_airport = ?",
                       (airport_id))
        flights = cursor.fetchall()
        print("\nFlights for airport {}:".format(airport_id))
        for flight in flights:
            print(flight)

    elif choice == "6":
        # Display route_IDs and names
        cursor.execute(
            "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes"
        )
        routes = cursor.fetchall()
        print("\nRoutes:")
        for route in routes:
            print(route)
        # Ask user to input ID of route whose flights they wish to see
        route_id = input(
            "\nEnter the ID of the route whose flights you would like to view: ")
        # Display flights for that route by date
        cursor.execute("SELECT * FROM Flights WHERE route_ID = ?", (route_id,))
        flights = cursor.fetchall()
        print("\nFlights for route {}:".format(route_id))
        for flight in flights:
            print(flight)

    elif choice == "7":
        return


# VIEW PILOTS FUNCTION

def view_pilots():
    print("\n1. View All Pilots")
    print("2. View Pilots by Age")
    print("3. View Pilots by Nationality")
    print("4. View Pilots by Flight")
    print("5. Return to Main Menu")
    choice = input("\nEnter your choice (1-5): ")
    if choice == "1":
        cursor.execute(
            "SELECT * FROM Pilots"
        )
        pilots = cursor.fetchall()
        print("\nAll Pilots:")
        print("\nID  | Name                | Nationality ID | Age")
        print("-" * 50)
        for pilot in pilots:
            print("{:4} | {:19} | {:14} | {}".format(pilot[0], pilot[1], pilot[2],
                                                     pilot[3]))
    elif choice == "2":
        # Ask user to input age
        age = input("Enter age: ")
        # Display pilots by age
        cursor.execute(
            "SELECT pilot_ID, pilot_name FROM Pilots WHERE pilot_age = ?", (age,))
        pilots = cursor.fetchall()
        print("\nPilots with age {}:".format(age))
        for pilot in pilots:
            print(pilot)
    elif choice == "3":
        # Ask user to input nationality
        nationality = input("Enter nationality: ")
        # Display pilots by nationality
        cursor.execute(
            "SELECT pilot_ID, pilot_name FROM Pilots WHERE pilot_nationality = ?",
            (nationality,))
        pilots = cursor.fetchall()
        print("\nPilots with nationality {}:".format(nationality))
        for pilot in pilots:
            print(pilot)
    elif choice == "4":
        # Ask user to input flight ID
        flight_id = input("Enter flight ID: ")
        # Display pilots by flight ID
        cursor.execute(
            "SELECT pilot_ID, pilot_name FROM Pilots WHERE pilot_ID = ?",
            (flight_id,))
        pilots = cursor.fetchall()
        print("\nPilots on flight {}:".format(flight_id))
        for pilot in pilots:
            print(pilot)
    elif choice == "5":
        return


# VIEW AIRPORTS FUNCTION

def view_airports():
    print("\n1. View All Airports")
    print("2. View Airports by Country")
    print("3. View Airports by City")
    print("4. Return to Main Menu")
    choice = input("\nEnter your choice (1-5): ")
    if choice == "1":
        cursor.execute("""
        SELECT * FROM Airports
        JOIN Cities ON Airports.city_ID = Cities.city_ID
        JOIN Countries ON Cities.country_ID = Countries.country_ID
    """)
        airports = cursor.fetchall()
        print("\nAll Airports:")
        print(
            "\nCode | Airport Name                           | City          | Country"
        )
        print("-" * 70)
        for airport in airports:
            print("{} | {:<35} | {:<13} | {}".format(airport[0], airport[1],
                                                     airport[2], airport[3]))
    elif choice == "2":
        # Ask user to input country
        country = input("Enter country: ")
        # Display airports by country
        cursor.execute(
            "SELECT airport_ID, airport_name, airport_city, airport_country FROM Airports WHERE airport_country = ?",
            (country,))
        airports = cursor.fetchall()
        print("\nAirports in {}:".format(country))
        for airport in airports:
            print(airport)
    elif choice == "3":
        # Ask user to input city
        city = input("Enter city: ")
        # Display airports by city
        cursor.execute(
            "SELECT airport_ID, airport_name, airport_city, airport_country FROM Airports WHERE airport_city = ?",
            (city,))
        airports = cursor.fetchall()
        print("\nAirports in {}:".format(city))
        for airport in airports:
            print(airport)
    elif choice == "4":
        return


# VIEW ROUTES FUNCTION

def view_routes():
    print("\n1. View All Routes")
    print("2. View Routes by Departure Airport")
    print("3. View Routes by Arrival Airport")
    print("4. View Routes by Duration")
    print("5. Return to Main Menu")
    choice = input("\nEnter your choice (1-5): ")
    if choice == "1":
        cursor.execute(
            "SELECT * FROM Routes"
        )
        routes = cursor.fetchall()
        print("\nAll Routes:")
        print("\nRoute ID | From  | To    | Duration (mins)")
        print("-" * 45)
        for route in routes:
            print("{:<9} | {:<5} | {:<5} | {:<8}".format(route[0], route[1],
                                                         route[2], route[3]))
    elif choice == "2":
        # Ask user to input departure airport
        departure_airport = input("Enter departure airport: ")
        # Display routes by departure airport
        cursor.execute(
            "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes WHERE departure_airport = ?",
            (departure_airport,))
        routes = cursor.fetchall()
        print("\nRoutes departing from {}:".format(departure_airport))
        for route in routes:
            print(route)
    elif choice == "3":
        # Ask user to input arrival airport
        arrival_airport = input("Enter arrival airport: ")
        # Display routes by arrival airport
        cursor.execute(
            "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes WHERE arrival_airport = ?",
            (arrival_airport,))
        routes = cursor.fetchall()
        print("\nRoutes arriving at {}:".format(arrival_airport))
        for route in routes:
            print(route)
    elif choice == "4":
        # Ask user to input duration
        duration = input("Enter duration (mins): ")
        # Display routes by duration
        cursor.execute(
            "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes WHERE duration = ?",
            (duration,))
        routes = cursor.fetchall()
        print("\nRoutes with duration {} minutes:".format(duration))
        for route in routes:
            print(route)
    elif choice == "5":
        return


# UPDATE FLIGHT FUNCTION

def update_flight():
    # Ask which flight the user would like to update by flight_ID
    flight_id = input("Enter the flight ID you would like to update: ")
    # Display all flights
    cursor.execute("SELECT * FROM Flights")
    flights = cursor.fetchall()
    print("\nAll Flights:")
    for flight in flights:
        print(flight)
    # Ask user which detail they would like to change
    print("\nWhich detail would you like to update?")
    print("1. Pilot")
    print("2. Departure Date/Time")
    print("3. Destination airport")
    choice = input("\nEnter your choice (1-3): ")
    # Update flight details based on user's choice
    if choice == "1":
        # Ask user to input new pilot_ID
        pilot_id = input("Enter the new pilot ID: ")
        # Update flight with new pilot_ID
        cursor.execute("UPDATE Flights SET pilot_ID = ? WHERE flight_ID = ?",
                       (pilot_id, flight_id))
        print("Flight {} updated successfully.".format(flight_id))
    elif choice == "2":
        # Ask user to input new departure_datetime
        departure_datetime = input(
            "Enter the new departure datetime (YYYY-MM-DD HH:MM): ")
        # Update flight with new departure_datetime
        cursor.execute(
            "UPDATE Flights SET departure_datetime = ? WHERE flight_ID = ?",
            (departure_datetime, flight_id))
        print("Flight {} updated successfully.".format(flight_id))
    elif choice == "3":
        # Ask user to input new arrival_airport_ID
        arrival_airport_id = input("Enter the new arrival airport ID: ").upper()

        # Verify route exists
        cursor.execute(
            "SELECT route_ID FROM Routes WHERE departure_airport = ? AND arrival_airport = ?",
            (departure_airport, arrival_airport_id))
        route = cursor.fetchone()

        if route is None:
            print("Route from {} to {} does not exist.".format(departure_airport, arrival_airport_id))
            return
        else:
            # Update the flight with the specified new arrival airport
            cursor.execute(
                "UPDATE Flights SET arrival_airport = ? WHERE flight_ID = ?",
                (arrival_airport_id, flight_id))


# UPDATE PILOT FUNCTION

def update_pilot():
    # Show list of pilots
    cursor.execute(
        "SELECT pilot_ID, pilot_name, pilot_nationality, pilot_age FROM Pilots")
    pilots = cursor.fetchall()
    print("\nPilots:")
    for pilot in pilots:
        print(pilot)
    # Ask user to input pilot_ID of pilot they would like to update
    pilot_id = input(
        "\nEnter the pilot ID of the pilot you would like to update: ")
    # Ask which aspect they would like to update
    print("\nWhich detail would you like to update?")
    print("1. Pilot Name")
    print("2. Pilot Nationality")
    print("3. Pilot Age")
    choice = input("\nEnter your choice (1-3): ")
    # Update pilot details based on user's choice
    if choice == "1":
        # Change name to new inputted name
        new_name = input("Enter the new pilot name: ")
        cursor.execute("UPDATE Pilots SET pilot_name = ? WHERE pilot_ID = ?",
                       (new_name, pilot_id))
        print("Pilot {} updated successfully.".format(pilot_id))
    elif choice == "2":
        # Change nationality to new inputted nationality
        new_nationality = input("Enter the new pilot nationality: ")
        cursor.execute(
            "UPDATE Pilots SET pilot_nationality = ? WHERE pilot_ID = ?",
            (new_nationality, pilot_id))
        print("Pilot {} updated successfully.".format(pilot_id))
    elif choice == "3":
        # Change age to new inputted age
        new_age = input("Enter the new pilot age: ")
        # Check if age valid
        try:
            new_age = int(new_age)
            if new_age < 18 or new_age > 65:
                print("Pilot must be between 18 and 65 years old.")
                return
            cursor.execute("UPDATE Pilots SET pilot_age = ? WHERE pilot_ID = ?",
                           (new_age, pilot_id))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        print("Pilot {} updated successfully.".format(pilot_id))


# UPDATE AIRPORT FUNCTION

def update_airport():
    # Show list of destinations
    cursor.execute(
        "SELECT airport_ID, airport_name, airport_city, airport_country FROM Airports"
    )
    destinations = cursor.fetchall()
    print("\nDestinations:")
    for destination in destinations:
        print(destination)
    # Ask user to input destination_ID of destination they would like to update
    destination_id = input(
        "\nEnter the destination ID of the destination you would like to update: "
    )
    # Ask which aspect they would like to update
    print("\nWhich detail would you like to update?")
    print("1. Destination Name")
    print("2. Destination City")
    print("3. Destination Country")
    choice = input("\nEnter your choice (1-3): ")
    # Update destination details based on user's choice
    if choice == "1":
        # Change name to new inputted name
        new_name = input("Enter the new destination name: ")
        cursor.execute("UPDATE Airports SET airport_name = ? WHERE airport_ID = ?",
                       (new_name, destination_id))
        print("Destination {} updated successfully.".format(destination_id))
    elif choice == "2":
        # Change city to new inputted city
        new_city = input("Enter the new destination city: ")
        cursor.execute("UPDATE Airports SET airport_city = ? WHERE airport_ID = ?",
                       (new_city, destination_id))
        print("Destination {} updated successfully.".format(destination_id))
    elif choice == "3":
        # Change country to new inputted country
        new_country = input("Enter the new destination country: ")
        cursor.execute(
            "UPDATE Airports SET airport_country = ? WHERE airport_ID = ?",
            (new_country, destination_id))
        print("Destination {} updated successfully.".format(destination_id))


# UPDATE ROUTE FUNCTION

def update_route():
    cursor.execute(
        "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes"
    )
    routes = cursor.fetchall()
    print("\nRoutes:")
    for route in routes:
        print(route)
    # Ask user to input route_ID of route they would like to update
    route_id = input(
        "\nEnter the route ID of the route you would like to update: ")
    # Ask which aspect they would like to update
    print("\nWhich detail would you like to update?")
    print("1. Route Departure Airport")
    print("2. Route Arrival Airport")
    choice = input("\nEnter your choice (1-2): ")
    # Update route details based on user's choice
    if choice == "1":
        # Change departure airport to new inputted departure airport
        new_departure_airport = input("Enter the new departure airport: ")
        # Check route doesn't already exist
        new_arrival_airport = cursor.execute(
            "SELECT arrival_airport FROM Routes WHERE route_ID = ?", (route_id,)).fetchone()[0]
        cursor.execute(
            "SELECT * FROM Routes WHERE departure_airport = ? AND arrival_airport = ?",
            (new_departure_airport, new_arrival_airport))
        if not cursor.fetchone():
            cursor.execute(
                "UPDATE Routes SET departure_airport = ? WHERE route_ID = ?",
                (new_departure_airport, route_id))
            print("Route {} updated successfully.".format(route_id))
    elif choice == "2":
        # Change arrival airport to new inputted arrival airport
        new_arrival_airport = input("Enter the new arrival airport: ")
        # Check route doesn't already exist
        cursor.execute(
            "SELECT * FROM Routes WHERE departure_airport = ? AND arrival_airport = ?",
            (new_departure_airport, new_arrival_airport))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE Routes SET arrival_airport = ? WHERE route_ID = ?",
                (new_arrival_airport, route_id))
            print("Route {} updated successfully.".format(route_id))


# DELETE FLIGHT FUNCTION

def delete_flight():
    # Show list of flights
    cursor.execute("""
      SELECT Flights.flight_ID, Pilots.pilot_name, Routes.departure_airport, 
             Routes.arrival_airport, Flights.departure_datetime, Routes.duration
      FROM Flights
      JOIN Pilots ON Flights.pilot_ID = Pilots.pilot_ID
      JOIN Routes ON Flights.route_ID = Routes.route_ID
  """)
    flights = cursor.fetchall()
    print("\nFlights:")
    for flight in flights:
        print(flight)
    # Ask user to input flight_ID of flight they would like to delete
    flight_id = input(
        "\nEnter the flight ID of the flight you would like to delete: ")
    # Confirm wish to delete flight
    confirm = input(
        "\nAre you sure you want to delete flight {}? (Y/N): ".format(flight_id))
    if confirm.upper() == "Y":
        # Delete flight
        cursor.execute("DELETE FROM Flights WHERE flight_ID = ?", (flight_id,))
        print("Flight {} deleted successfully.".format(flight_id))
    else:
        print("Deletion cancelled.")
    return


# DELETE PILOT FUNCTION

def delete_pilot():
    # Show list of pilots
    cursor.execute("SELECT pilot_ID, pilot_name FROM Pilots")
    pilots = cursor.fetchall()
    print("\nPilots:")
    for pilot in pilots:
        print(pilot)
    # Ask user to input pilot_ID of pilot they would like to delete
    pilot_id = input(
        "\nEnter the pilot ID of the pilot you would like to delete: ")
    # Confirm wish to delete pilot
    confirm = input(
        "\nAre you sure you want to delete pilot {}? (Y/N): ".format(pilot_id))
    if confirm.upper() == "Y":
        # Delete pilot
        cursor.execute("DELETE FROM Pilots WHERE pilot_ID = ?", (pilot_id,))
        print("Pilot {} deleted successfully.".format(pilot_id))
    else:
        print("Deletion cancelled.")
    return


# DELETE AIRPORT FUNCTION

def delete_airport():
    # Show all airports with their cities and countries
    cursor.execute("""
      SELECT Airports.airport_ID, Airports.airport_name, Cities.city_name, Countries.country_name 
      FROM Airports
      JOIN Cities ON Airports.city_ID = Cities.city_ID
      JOIN Countries ON Cities.country_ID = Countries.country_ID
  """)
    airports = cursor.fetchall()
    print("\nAirports:")
    for airport in airports:
        print("ID: {}, Name: {}, City: {}, Country: {}".format(airport[0], airport[1], airport[2], airport[3]))

    # Ask user to input airport_ID of airport they would like to delete
    airport_id = input("\nEnter the airport ID you would like to delete: ").upper()

    # Confirm wish to delete airport
    confirm = input(
        "\nAre you sure you want to delete airport {}? This will delete all routes using this airport. (Y/N): "
        .format(airport_id))
    if confirm.upper() == "Y":
        cursor.execute("DELETE FROM Airports WHERE airport_ID = ?", (airport_id,))
        print("Airport {} deleted successfully.".format(airport_id))


# DELETE ROUTE FUNCTION

def delete_route():
    # Show all routes
    cursor.execute(
        "SELECT route_ID, departure_airport, arrival_airport, duration FROM Routes"
    )
    routes = cursor.fetchall()
    print("\nRoutes:")
    for route in routes:
        print(route)
    # Ask user to input route_ID of route they would like to delete
    route_id = input(
        "\nEnter the route ID of the route you would like to delete: ")
    # Confirm wish to delete route
    confirm = input(
        "\nAre you sure you want to delete route {}? (Y/N): ".format(route_id))
    if confirm.upper() == "Y":
        # Get route details to find return route
        cursor.execute("SELECT departure_airport, arrival_airport FROM Routes WHERE route_ID = ?", (route_id,))
        route = cursor.fetchone()
        if route:
            # Delete the specified route
            cursor.execute("DELETE FROM Routes WHERE route_ID = ?", (route_id,))
            # Delete the return route if it exists
            cursor.execute("DELETE FROM Routes WHERE departure_airport = ? AND arrival_airport = ?",
                           (route[1], route[0]))
            print("Route {} and its return route (if any) deleted successfully.".format(route_id))
    else:
        print("Deletion cancelled.")


print("\nFlight Management System ready. Click return to begin.")
input()

### MAIN MENU LOGIC ###

while True:
    print("\nFlight Management System: Main Menu\n")
    print("\n1. Add New Flight/Pilot/Airport/Route")
    print("2. View Flight/Pilot/Airport/Route Records")
    print("3. Update Flight/Pilot/Airport/Route Information")
    print("4. Delete Flight/Pilot/Airport/Route Record")
    print("5. Exit")
    choice = input("\nEnter your choice (1-5): ")

    # If user chooses to add new flight/pilot/airport/route
    if choice == "1":
        print("\n1. Add New Flight")
        print("2. Add New Pilot")
        print("3. Add New Airport")
        print("4. Add New Route")
        print("5. Return to Main Menu")
        choice = input(
            "\nEnter the number of the action you would like to perform: ")
        if choice == "1":
            add_flight()
        elif choice == "2":
            add_pilot()
        elif choice == "3":
            add_airport()
        elif choice == "4":
            add_route()
        elif choice == "5":
            continue
        else:
            print(f"{choice} is not a valid option. Please try again.")

    # If user chooses to view flight/pilot/airport/route records
    elif choice == "2":
        print("\n1. View Flight Records")
        print("2. View Pilot Records")
        print("3. View Airport Records")
        print("4. View Route Records")
        print("5. Return to Main Menu")
        choice = input(
            "\nEnter the number of the action you would like to perform: ")
        if choice == "1":
            view_flights()
        elif choice == "2":
            view_pilots()
        elif choice == "3":
            view_airports()
        elif choice == "4":
            view_routes()
        elif choice == "5":
            continue
        else:
            print(f"{choice} is not a valid option. Please try again.")

    # If user chooses to update flight/pilot/destination/route information
    elif choice == "3":
        print("\n1. Update Flight Record")
        print("2. Update Pilot Record")
        print("3. Update Airport Record")
        print("4. Update Route Record")
        print("5. Return to Main Menu")
        choice = input(
            "\nEnter the number of the action you would like to perform: ")
        if choice == "1":
            update_flight()
        elif choice == "2":
            update_pilot()
        elif choice == "3":
            update_airport()
        elif choice == "4":
            update_route()
        elif choice == "5":
            continue
        else:
            print("{} is not a valid option. Please try again.".format(choice))

    # If user chooses to delete flight/pilot/destination/route record
    elif choice == "4":
        print("\n1. Delete Flight Record")
        print("2. Delete Pilot Record")
        print("3. Delete Airport Record")
        print("4. Delete Route Record")
        print("5. Return to Main Menu")
        choice = input(
            "\nEnter the number of the action you would like to perform: ")
        if choice == "1":
            delete_flight()
        elif choice == "2":
            delete_pilot()
        elif choice == "3":
            delete_airport()
        elif choice == "4":
            delete_route()
        elif choice == "5":
            continue
        else:
            print("{} is not a valid option. Please try again.".format(choice))

    # If user chooses to exit
    elif choice == "5":
        print("\nExiting Flight Management System...")
        break
    # If user enters an invalid choice
    else:
        print("Invalid input. Please try again.")

conn.commit()
conn.close()
