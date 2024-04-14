from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_transactions_from_db, load_transaction_from_db, add_new_transaction, get_initial_balance, get_categories
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    try:
        transactions = load_transactions_from_db()

        initial_balance = get_initial_balance()

        balance = initial_balance

        for transaction in transactions:
            balance += transaction['income']
            balance -= transaction['expense']
            transaction['balance'] = balance

        transactions.reverse()
        print(type(transactions))
        #this executes the page
        return render_template('home.html',transactions=transactions,balance=balance, initial_balance=initial_balance)
    except Exception as e:
        return "Data base not available or has a problem"

@app.route("/api/transactions")
def list_transactions():
    transactions = load_transactions_from_db()
    return jsonify(transactions)

@app.route("/transaction/<id>")
def show_transact(id):
    transact = load_transaction_from_db(id)
    return jsonify(transact)

@app.route("/new")
def new_transaction():    

    categories = get_categories()

    today = datetime.now().strftime("%Y-%m-%d")

    print(today)

    #this executes the page
    return render_template('new_transaction.html',categories=categories,today=today)

@app.route("/submit", methods=['POST'])
def submit():
    # Handle POST request
    data = request.form

    add_new_transaction(data)    

    #this executes the page
    return redirect(url_for('index'))
    #return jsonify(data)


#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
