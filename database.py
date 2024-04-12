from sqlalchemy import create_engine, text
import os

with open('SECRET.txt','r') as file:
    connection_string = file.read()

engine = create_engine(str(connection_string)).execution_options(isolation_level="AUTOCOMMIT")

def get_initial_balance():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM transactions WHERE category = 'Initial Balance';"))
      
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction['income']  

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from transactions where category <> 'Initial Balance' order by id asc;"))
      
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
        

def add_new_transaction(data):
    with engine.connect() as conn:
        query = text("INSERT INTO transactions (date,category,[desc],income,outcome) VALUES (:date, :category, :description, :income, :outcome)")        
        
        response = conn.execute(query,{"date":data['Date'],"category":data['Category'],"description":data['Description'],"income":data['Income'],"outcome":data['Outcome']})
        #response = conn.execute(query,date=data['Date'],category=data['Category'],description=data['Description'],income=data['Income'],outcome=data['Outcome'])
       
        return response