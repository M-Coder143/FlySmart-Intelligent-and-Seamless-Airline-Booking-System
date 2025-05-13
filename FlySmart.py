from datetime import datetime

# Mock Database
flight_database = []
user_profiles = {}
booking_history = []

# Utils

def validate_credentials(email, password):
    return email in user_profiles and user_profiles[email]['password'] == password

def create_user(name, email, password, role="customer"):
    user_profiles[email] = {'name': name, 'password': password, 'role': role}

def get_user(email):
    return user_profiles.get(email)

def book_flight(flight_id, passenger_info, user_email):
    flight = next((f for f in flight_database if f['id'] == flight_id), None)
    if flight and flight['seats'] > 0:
        flight['seats'] -= 1
        booking = {'user': user_email, 'flight_id': flight_id, 'passenger': passenger_info}
        booking_history.append(booking)
        return "Booking Confirmed!"
    return "Booking Failed."

def fetch_bookings(user_email):
    return [b for b in booking_history if b['user'] == user_email]

def generate_recommendations(user_email):
    return ["Paris", "Tokyo", "New York", "Dubai", "Singapore", "London", "Sydney", "Rome", "Bangkok", "Toronto"]

def search_flights(departure, destination, date):
    matching_flights = [
        f for f in flight_database
        if f['from'] == departure and f['to'] == destination and f['date'] == date and f['seats'] > 0
    ]
    return sorted(matching_flights, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))

# Admin Features
def all_bookings():
    return booking_history

def manage_flights():
    print("Admin Flight Management Options (mock)")

# Sample Data
flight_database.append({'id': 'F001', 'from': 'NYC', 'to': 'LAX', 'date': '2025-05-01', 'seats': 10})
flight_database.append({'id': 'F002', 'from': 'NYC', 'to': 'LAX', 'date': '2025-05-02', 'seats': 5})
flight_database.append({'id': 'F003', 'from': 'NYC', 'to': 'PAR', 'date': '2025-05-03', 'seats': 8})
flight_database.append({'id': 'F004', 'from': 'LAX', 'to': 'NYC', 'date': '2025-05-04', 'seats': 6})
flight_database.append({'id': 'F005', 'from': 'NYC', 'to': 'TOK', 'date': '2025-05-05', 'seats': 12})
flight_database.append({'id': 'F006', 'from': 'LAX', 'to': 'CHI', 'date': '2025-05-06', 'seats': 9})
flight_database.append({'id': 'F007', 'from': 'CHI', 'to': 'MIA', 'date': '2025-05-07', 'seats': 7})
flight_database.append({'id': 'F008', 'from': 'MIA', 'to': 'NYC', 'date': '2025-05-08', 'seats': 10})
flight_database.append({'id': 'F009', 'from': 'TOK', 'to': 'LAX', 'date': '2025-05-09', 'seats': 5})
flight_database.append({'id': 'F010', 'from': 'PAR', 'to': 'NYC', 'date': '2025-05-10', 'seats': 4})

# Main App
authenticated = False
current_user_email = None
user_role = None

while not authenticated:
    print("\nWelcome to FlySmart!")
    print("1. Log In\n2. Sign Up\n3. Forgot Password\n4. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        email = input("Email: ")
        password = input("Password: ")
        if validate_credentials(email, password):
            authenticated = True
            current_user_email = email
            user_role = get_user(email)['role']
            print("Login successful!")
        else:
            print("Invalid credentials.")

    elif choice == '2':
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        if email not in user_profiles:
            create_user(name, email, password)
            print("Sign up successful. Please log in.")
        else:
            print("Email already registered.")

    elif choice == '3':
        email = input("Enter your email: ")
        if email in user_profiles:
            print(f"Password reset link sent to {email} (mock)")
        else:
            print("Email not found.")

    elif choice == '4':
        print("Thank you for visiting FlySmart!")
        break

    else:
        print("Invalid choice.")

# Main Menu
while authenticated:
    print(f"\nWelcome {get_user(current_user_email)['name']} ({user_role})")
    if user_role == "admin":
        print("1. View All Bookings\n2. Manage Flights\n3. Log Out")
        admin_choice = input("Choose an option: ")
        if admin_choice == '1':
            print(all_bookings())
        elif admin_choice == '2':
            manage_flights()
        elif admin_choice == '3':
            authenticated = False
            print("Logged out.")
        else:
            print("Invalid option.")
    else:
        print("1. Search Flights\n2. Smart Recommendations\n3. View Bookings\n4. Log Out")
        user_choice = input("Choose an option: ")

        if user_choice == '1':
            from_city = input("From: ")
            to_city = input("To: ")
            date = input("Date (YYYY-MM-DD): ")
            results = search_flights(from_city, to_city, date)
            print("Flights:", results)
            if results:
                book = input("Book a flight? (yes/no): ")
                if book.lower() == 'yes':
                    flight_id = input("Enter Flight ID: ")
                    passenger = input("Passenger Name: ")
                    print(book_flight(flight_id, passenger, current_user_email))

        elif user_choice == '2':
            print("Recommendations:", generate_recommendations(current_user_email))

        elif user_choice == '3':
            print("Your Bookings:", fetch_bookings(current_user_email))

        elif user_choice == '4':
            authenticated = False
            print("Logged out.")
        else:
            print("Invalid option.")
