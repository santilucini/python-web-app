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
    
def load_transaction_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from transactions where id= :val"),
                              {"val": id})
      
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction   