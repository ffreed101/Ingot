import sqlite3
import json
from models.User import User

# TODO: Add a transactions attribute to user class that modifies the balance, as well as adding user-side functionality to add, edit, view, and remove transactions in user_menu. Transactions might be separate data table

# SQLite functionality
con = sqlite3.connect("database.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE users (
                first text,
                last text,
                balance real,
                fixed_expenses text
        )""")
    print("Formatting data...")
except:
    print("Data found")

def insert_user(user):
    with con:
        cur.execute("INSERT INTO users VALUES (:first, :last, :balance, :fixed_expenses)", {"first": user.first, "last": user.last, "balance": user.balance, "fixed_expenses": user.fixed_expenses_str})

def update_balance(user, balance):
    with con:
        cur.execute("""UPDATE users SET balance = :balance 
                    WHERE first = :first AND last = :last""", 
                    {'first': user.first, 'last': user.last, 'balance': balance})
        
def update_fixed_expenses(user, fixed_expenses):
    with con:
        cur.execute("""UPDATE users SET fixed_expenses = :fixed_expenses 
                    WHERE first = :first AND last = :last""", 
                    {'first': user.first, 'last': user.last, 'fixed_expenses': fixed_expenses})

def remove_user(user):
    with con:
        cur.execute("DELETE from users WHERE first = :first AND last = :last", 
                    {"first": user.first, "last": user.last})

def get_user_by_name(first_name):
    cur.execute("SELECT * FROM users WHERE first=:first", {"first": first_name})
    return cur.fetchone()

# Utility functions
def list_users():
    cur.execute("SELECT first, last FROM users")
    users = cur.fetchall()
    for i, user in enumerate(users, 1):
        print(f"{i}. {user[0]} {user[1]}")
    return users

# Program functionality
def create_user():
    first = input("Enter first name: ").capitalize()
    last = input("Enter last name: ").capitalize()
    init_balance = float(input("Enter initial balance: "))
    fixed_expenses = get_fixed_expenses()
    insert_user(User(first, last, init_balance, fixed_expenses, ))

def select_user():
    while True:
        selected = input("Enter user's first name: ").capitalize()
        try:
            attribute_list = get_user_by_name(selected)
            return User(attribute_list[0], attribute_list[1], attribute_list[2], json.loads(attribute_list[3]))
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

def get_fixed_expenses():
    expenses = {}
    while True:
        name = input("Enter expense name(Leave blank when finished): ")
        if name == "":
            break
        amount = float(input("Enter expense amount: "))
        expenses[name] = amount
    return expenses

def main():
    while True:
        print("Main Menu")
        print("1. Log In")
        print("2. Create user")
        print("3. List all Users")
        print("4. Exit")
        choice = int(input("Enter a choice: "))
        match choice:
            case 1:
                user_menu()
            case 2:
                create_user()
            case 3:
                list_users()
            case 4:
                break

main()
con.close()