from sqlalchemy import create_engine, text

#engine = create_engine("mssql+pyodbc://sa:GT4Y8KjzXCjhcB@mydsn")

engine = create_engine("mssql+pymssql://sa:GT4Y8KjzXCjhcB@192.168.0.18:1433/Expenses")

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from transactions;"))

        transactions = []
        for row in result.all():
            transactions.append(dict(row._mapping))

        return transactions