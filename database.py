from sqlalchemy import create_engine, text, insert
import os

# Get the directory of the script
script_dir = os.path.dirname(__file__)
# Construct the full path to the file
file_path = os.path.join(script_dir, 'SECRET.txt')

with open(file_path,'r') as file:
    connection_string = file.read()

engine = create_engine(str(connection_string)).execution_options(isolation_level="AUTOCOMMIT")

def get_initial_balance(id_category,field):
    with engine.connect() as conn:
        query = "SELECT "+field+" as amount FROM transactions WHERE category = :id_category;"
        result = conn.execute(text(query),{"field":field,"id_category":id_category})
      
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction['amount']

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id,date,c.Category as category,t.description as description,amount_arg,amount_usd,type FROM transactions AS t LEFT JOIN categories AS c ON t.category=c.id_category WHERE c.id_category<>1"))
      
        transactions = []
        for row in result.all():
            transactions.append(dict(row._mapping))

        return transactions
    
def load_transaction_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("select id,c.id_category,c.Category as category,t.description,date,type,amount_arg,amount_usd from transactions t inner join categories c ON t.category = c.id_category where id = :val"),
                              {"val": id})
      
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction   

def load_from_db_by_category(id_category):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id,date,c.Category as category,t.description as description,amount_arg,amount_usd,type FROM transactions AS t LEFT JOIN categories AS c ON t.category=c.id_category WHERE c.id_category = :id_category"),
                              {"id_category":id_category})
      
        transactions = []
        for row in result.all():
            transactions.append(dict(row._mapping))

        return transactions
        

def add_new_transaction(data):
    with engine.connect() as conn:
        query = text("INSERT INTO transactions (date,category,description,type,amount_arg,amount_usd) VALUES (:date, :category, :description, :type, :amount_arg, :amount_usd)")       
        
        response = conn.execute(query,{"date":data['Date'],"category":data['Category'],"description":data['Description'],"type":data['Type'],"amount_arg":data['Amount_ARG'],"amount_usd":data['Amount_USD']})
        #response = conn.execute(query,date=data['Date'],category=data['Category'],description=data['Description'],income=data['Income'],outcome=data['Outcome'])
        
        return response

def add_new_transaction_saving(data):
    with engine.connect() as conn:
        query = text("INSERT INTO savings (id_transaction,amount) VALUES (:id_transaction, :amount)")       
        
        response = conn.execute(query,{"id_transaction":data['id_transaction'],"amount":data['amount']})        
        
        return response

def update_transaction(data):
    with engine.connect() as conn:
        query = text("UPDATE [dbo].[transactions] SET [category] = :category,[description] = :description,[date] = :date,[type] = :type,[amount_arg] = :amount_arg, [amount_usd] = :amount_usd WHERE [id] = :id")        
        
        response = conn.execute(query,{"date":data['Date'],"category":data['Category'],"description":data['Description'],"type":data['Type'],"amount_arg":data['Amount_ARG'],"amount_usd":data['Amount_USD'],"id":data['id']})        
       
        return response

def get_categories():
    with engine.connect() as conn:
        result = conn.execute(text("select * from categories where id_category <> 1;"))
      
        categories = []
        for row in result.all():
            categories.append(dict(row._mapping))

        return categories
    

def get_last_inserted():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT Max(id) as Last_ID FROM transactions"))   
       
        rows = result.all()        
        if len(rows) == 0:
            return None
        else:  
            for row in rows:
                transaction = dict(row._mapping)
            return transaction['Last_ID']