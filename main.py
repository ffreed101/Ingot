import json
from models import session, User, Transaction
from activate import ensure_virtualenv

ensure_virtualenv()

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
                    edit_balance(user)
                case 2:
                    transactions_menu(user)
                case 3:
                    user_deleted = delete_user(user)
                    if user_deleted:
                        break
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
                transaction = select_transaction(user)
                edit_transaction_value(transaction)
            case 3:
                list_transactions(user)
            case 4:
                delete_transaction(user)
            case 5:
                break

# Create Functions

def add_transaction(user_id, date, category, amount, note):
    new_transaction = Transaction(user_id=user_id, date=date, category=category, amount=amount, note=note)
    session.add(new_transaction)
    session.commit()

def create_transaction(user):
    user_id = user.id
    date = "Not Implemented"
    category = get_category()
    amount = float(input("Enter transaction amount: "))
    note = input("Add a note: ")
    add_transaction(user_id, date, category, amount, note)

def create_user():
    first = input("Enter first name: ").capitalize()
    last = input("Enter last name: ").capitalize()
    init_balance = float(input("Enter initial balance: "))
    fixed_expenses = json.dumps(get_fixed_expenses())
    new_user = User(first=first, last=last, fixed_expenses=fixed_expenses)
    session.add(new_user)
    session.commit()
    add_transaction(new_user.id, "Not Implemented", "System", init_balance, "Initialized balance")

# Update Functions

def update_balance(user, new_balance):
    transaction_amount = new_balance - user.balance
    add_transaction(user.id, "Not Implemented", "System", transaction_amount, "Balance adjustment")
    
def edit_balance(user):
    new_balance = float(input("Enter new balance: "))
    update_balance(user, new_balance)

def edit_transaction_value(transaction):
    while True:
        print(f"Editing {transaction.note} transaction from {transaction.date}...")
        print("1. Note")
        print("2. Category")
        print("3. Amount")
        print("4. Exit")
        choice = int(input("Select a value to modify: "))

        match choice:
            case 1:
                new_note = input("Enter a new note: ")
                transaction.note = new_note
                session.commit()
                break
            case 2:
                new_category = get_category()
                transaction.category = new_category
                session.commit()
                break
            case 3:
                new_amount = float(input("Enter new amount: "))
                transaction.amount = new_amount
                session.commit()
                break
            case 4:
                break
            case _:
                print("Invalid input.")

# Delete Functions

def delete_transaction(user):
    transaction = select_transaction(user)
    session.delete(transaction)
    session.commit()
    print("Transaction deleted successfully")

def delete_user(user):
    while True:
        choice = input(f"Are you sure you want to delete user {user.first} {user.last}?(Y/N): ").lower()
        if choice == 'y':
            session.delete(user)
            session.commit()
            print("User Deleted")
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input.")

# Utility Functions

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
    user = input("Enter user's first name: ").capitalize()
    selected = session.query(User).filter_by(first=user).one_or_none()
    if selected == None:
        print("User not found.")
    else:
        return selected
    
def select_transaction(user):
    list_transactions(user)
    transaction_id = int(input("Enter desired transaction ID: "))
    transaction = session.query(Transaction).filter_by(id=transaction_id).one_or_none()
    return transaction
    
def list_users():
    users = session.query(User).all()
    for i in users:
        print(f"{i.first} {i.last}")

def list_transactions(user):
    transactions = session.query(Transaction).filter_by(user_id=user.id).all()
    labels = ("ID No.", "Note", "Category", "Amount", "Date")
    print(f"{labels[0]:^8}{labels[1]:^20}{labels[2]:^20}{labels[3]:^9}{labels[4]:^15}")
    for i in transactions:
        print(f"{i.id:^8}{i.note:^20}{i.category:^20}{i.amount:^9}{i.date:^15}") 

main()