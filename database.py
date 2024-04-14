from sqlalchemy import create_engine, text
import os

with open('SECRET.txt','r') as file:
    connection_string = file.read()

engine = create_engine(str(connection_string)).execution_options(isolation_level="AUTOCOMMIT")

def get_initial_balance():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM transactions WHERE category = '1';"))
      
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction['income']  

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id,date,c.Category as category,t.description as description,income,expense FROM transactions AS t LEFT JOIN categories AS c ON t.category=c.id_category WHERE c.id_category<>1"))
      
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
        query = text("INSERT INTO transactions (date,category,description,income,expense) VALUES (:date, :category, :description, :income, :expense)")        
        
        response = conn.execute(query,{"date":data['Date'],"category":data['Category'],"description":data['Description'],"income":data['Income'],"expense":data['Expense']})
        #response = conn.execute(query,date=data['Date'],category=data['Category'],description=data['Description'],income=data['Income'],outcome=data['Outcome'])
       
        return response

def get_categories():
    with engine.connect() as conn:
        result = conn.execute(text("select * from categories where id_category <> 1;"))
      
        categories = []
        for row in result.all():
            categories.append(dict(row._mapping))

        return categories