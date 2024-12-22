import sqlite3
from models.User import User

con = sqlite3.connect("database.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE users (
                first text,
                last text,
                balance real
        )""")
    print("Formatting data...")
except:
    print("Data found")

def insert_user(user):
    with con:
        cur.execute("INSERT INTO users VALUES (:first, :last, :balance)", {"first": user.first, "last": user.last, "balance": user.balance})

def update_balance(user, balance):
    with con:
        cur.execute("""UPDATE users SET balance = :balance 
                    WHERE first = :first AND last = :last""", 
                    {'first': user.first, 'last': user.last, 'balance': balance})

def remove_user(user):
    with con:
        cur.execute("DELETE from users WHERE first = :first AND last = :last", 
                    {"first": user.first, "last": user.last})

def get_user_by_name(first_name):
    cur.execute("SELECT * FROM users WHERE first=:first", {"first": first_name})
    return cur.fetchone()

def create_user():
    first = input("Enter first name: ").capitalize()
    last = input("Enter last name: ").capitalize()
    init_balance = float(input("Enter initial balance: "))
    insert_user(User(first, last, init_balance))

def select_user():
    while True:
        selected = input("Enter user's first name: ").capitalize()
        try:
            attribute_list = get_user_by_name(selected)
            return User(attribute_list[0], attribute_list[1], attribute_list[2])
        except:
            print("User not found.")

def user_menu():
    user = select_user()
    while True:
        print(f"{user.first} {user.last}")
        print(f"Balance: {user.balance:.2f}")
        print("1. Edit balance")
        print("2. Delete User")
        print("3. Back")
        choice = int(input("Enter a choice: "))
        match choice:
            case 1:
                new_balance = float(input("Enter new balance: "))
                user.balance = new_balance
                update_balance(user, user.balance)
                
            case 2:
                remove_user(user)
                break
            case 3:
                break

def main():
    while True:
        print("Main Menu")
        print("1. Log In")
        print("2. Create user")
        print("3. Exit")
        choice = int(input("Enter a choice: "))
        match choice:
            case 1:
                user_menu()
            case 2:
                create_user()
            case 3:
                break
main()

con.close()