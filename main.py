import sqlite3
import json
from models import session, User, Transaction

# TODO: Add a transactions attribute to user class that modifies the balance, as well as adding user-side functionality to add, edit, view, and remove transactions in user_menu. Transactions might be separate data table
        
# Menu Functions

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

def user_menu():
    user = select_user()
    if user != None:
        while True:
            print(f"{user.first} {user.last}")
            print(f"Balance: {user.balance:.2f}")
            print("1. Edit balance")
            print("2. Transactions")
            print("3. Delete User")
            print("4. Back")
            choice = int(input("Enter a choice: "))
            match choice:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    break
    else:
        pass

def transactions_menu(user):
    while True:
        print("Transactions Menu")
        print("1. Add Transaction")
        print("2. Edit Transaction")
        print("3. View All Transactions")
        print("4. Delete Transaction")
        print("5. Back")
        choice = int(input("Enter a choice: "))

        match choice:
            case 1:
                create_transaction(user)
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass

# Create Functions

def create_transaction(user):
    user_id = user.user_id
    date = "Not Implemented"
    category = get_category()
    amount = float(input("Enter transaction amount: "))
    note = input("Add a note: ")
    new_transaction = Transaction(user_id=user_id, date=date, category=category, amount=amount, note=note)
    session.add(new_transaction)
    session.commit()

def create_user():
    first = input("Enter first name: ").capitalize()
    last = input("Enter last name: ").capitalize()
    init_balance = float(input("Enter initial balance: "))
    fixed_expenses = json.dumps(get_fixed_expenses())
    new_user = User(first=first, last=last, balance=init_balance, fixed_expenses=fixed_expenses)
    session.add(new_user)
    session.commit()

# Update Functions

# Utility functions

def get_category():
    while True:
        print("Categories")
        print("1. Food")
        print("2. Recreation")
        print("3. Gas")
        print("4. Entertainment")
        print("5. Personal")
        print("6. Other")
        try:
            choice = int(input("Enter a choice: "))
        except:
            print("Please enter a number.")

        if choice == 1:
            return "Food"
        elif choice == 2:
            return "Recreation"
        elif choice == 3:
            return "Gas"
        elif choice == 4:
            return "Entertainment"
        elif choice == 5:
            return "Personal"
        elif choice == 6:
            return "Other"
        else:
            print("Choose the number that matches the category you want.")

def get_fixed_expenses():
    expenses = {}
    while True:
        name = input("Enter expense name(Leave blank when finished): ")
        if name == "":
            break
        amount = float(input("Enter expense amount: "))
        expenses[name] = amount
    return expenses

def select_user():
    user = input("Enter user's first name: ")
    selected = session.query(User).filter_by(first=user).one_or_none()
    if selected == None:
        print("User not found.")
    else:
        return selected
    
def list_users():
    users = session.query(User).all()
    for i in users:
        print(f"{i.first} {i.last}")

main()