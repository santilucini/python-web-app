from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_transactions_from_db, load_transaction_from_db, add_new_transaction, get_initial_balance, get_categories,update_transaction
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/expenses")
def index():
    try:
        transactions = load_transactions_from_db()

        initial_balance = get_initial_balance()

        balance = initial_balance

        for transaction in transactions:
            if transaction['type'] == 1:
                balance -= transaction['amount']
            elif transaction['type'] == 2:
                balance += transaction['amount']

            transaction['balance'] = balance

        transactions.reverse()
        #this executes the page
        return render_template('base.html',page='expenses.html',transactions=transactions,balance=balance, initial_balance=initial_balance)
    except Exception as e:
        return e

@app.route("/savings")
def savings():
    try:
        return render_template('base.html',page='savings.html')
    except Exception as e:
        return e

@app.route("/debts")
def debts():
    try:
        return render_template('base.html',page='debts.html')
    except Exception as e:
        return e

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

    #this executes the page
    return render_template('new_transaction.html',categories=categories,today=today)

@app.route("/edit/<id>")
def edit_transaction(id): 

    transaction = load_transaction_from_db(id)

    categories = get_categories()

    #this executes the page
    return render_template('edit_transaction.html',categories=categories,transaction=transaction)
    #return jsonify(transaction)

@app.route("/submit_new", methods=['POST'])
def submit_new():
    # Handle POST request
    data = request.form

    add_new_transaction(data)    

    #this executes the page
    return redirect(url_for('index'))
    #return jsonify(data)

@app.route("/submit_edit", methods=['POST'])
def submit_edit():
    # Handle POST request
    data = request.form

    update_transaction(data)    

    #this executes the page
    return redirect(url_for('index'))
    #return jsonify(data)


#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
