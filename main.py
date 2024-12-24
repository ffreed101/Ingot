import sqlite3
import json
from models.User import User
from models.Transaction import Transaction
# TODO: Add a transactions attribute to user class that modifies the balance, as well as adding user-side functionality to add, edit, view, and remove transactions in user_menu. Transactions might be separate data table

# SQLite functionality
con = sqlite3.connect("database.db")
cur = con.cursor()

try:
    cur.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first text,
                last text,
                balance real,
                fixed_expenses text
        )""")
    print("Formatting user data...")
except:
    print("User data found")

try:
    cur.execute("""CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                category TEXT,
                amount REAL,
                note TEXT,
                FOREIGN KEY (user_id) REFERENCES users (rowid)
        )""")
    print("Formatting transactions data...")
except:
    print("Transactions data found")

def insert_user(user):
    with con:
        cur.execute("INSERT INTO users (first, last, balance, fixed_expenses) VALUES (:first, :last, :balance, :fixed_expenses)", {"first": user.first, "last": user.last, "balance": user.balance, "fixed_expenses": user.fixed_expenses_str})

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

def get_user_by_id(user_id):
    cur.execute("SELECT * FROM users WHERE id=:id", {"id": user_id})
    return cur.fetchone()

# Transactions CRUD

def insert_transaction(transaction):
    with con:
        cur.execute("""INSERT INTO transactions (user_id, date, category, amount, note)
                       VALUES (:user_id, :date, :category, :amount, :note)""",
                    {'user_id': transaction.user_id,
                     'date': transaction.date,
                     'category': transaction.category,
                     'amount': transaction.amount,
                     'note': transaction.note})

def get_transactions_by_user(user_id):
    cur.execute("SELECT * FROM transactions WHERE user_id = :user_id", {"user_id": user_id})
    return cur.fetchall()

def delete_transaction(transaction_id):
    with con:
        cur.execute("DELETE FROM transactions WHERE id = :transaction_id", {"transaction_id": transaction_id})



# Utility functions
def list_users():
    print("Not Implemented")

# Program functionality
def create_user():
    first = input("Enter first name: ").capitalize()
    last = input("Enter last name: ").capitalize()
    init_balance = float(input("Enter initial balance: "))
    fixed_expenses = get_fixed_expenses()
    insert_user(User(first, last, init_balance, fixed_expenses))

def select_user():
    while True:
        selected = input("Enter user's first name(Leave blank to go back): ").capitalize()
        if selected == '':
            return None
        else:
            try:
                attribute_list = get_user_by_name(selected)
                return User(attribute_list[1], attribute_list[2], attribute_list[3], json.loads(attribute_list[4]))
            except:
                print("User not found.")

def user_menu():
    user = select_user()
    if user != None:
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
    else:
        pass

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