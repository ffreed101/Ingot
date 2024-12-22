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
    return cur.fetchall()

user_1 = User("Falon", "Freed", 300)
user_2 = User("Abigail", "Freed", 350)

print(get_user_by_name("Falon"))

con.close()