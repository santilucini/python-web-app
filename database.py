from sqlalchemy import create_engine, text
import os

with open('SECRET.txt','r') as file:
    connection_string = file.read()

engine = create_engine(str(connection_string))

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from transactions;"))
      
        transactions = []
        for row in result.all():
            transactions.append(dict(row._mapping))

        return transactions
    
print(load_transactions_from_db())