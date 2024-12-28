from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

db_path = "sqlite:///database.db"

engine = create_engine(db_path)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first = Column(String)
    last = Column(String)
    fixed_expenses = Column(String)
    transactions = relationship("Transaction", back_populates="user", lazy="dynamic")

    @property
    def balance(self):
        return self.transactions.with_entities(func.sum(Transaction.amount)).scalar() or 0
    

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    note = Column(String)
    category = Column(String)
    date = Column(String)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="transactions")

Base.metadata.create_all(engine)