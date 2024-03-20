from sqlalchemy import create_engine, text

engine = create_engine("")

def load_transactions_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from transactions;"))

        transactions = []
        for row in result.all():
            transactions.append(dict(row._mapping))

        return transactions