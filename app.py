from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_transactions_from_db, load_transaction_from_db, add_new_transaction, get_initial_balance

app = Flask(__name__)

@app.route("/")
def index():
    
    transactions = load_transactions_from_db()

    initial_balance = get_initial_balance()

    balance = initial_balance

    for transaction in transactions:
        balance += transaction['income']
        balance -= transaction['outcome']
        transaction['balance'] = balance

    transactions.reverse()
    print(type(transactions))
    #this executes the page
    return render_template('home.html',transactions=transactions,balance=balance, initial_balance=initial_balance)

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
    #this executes the page
    return render_template('new_transaction.html')

@app.route("/submit", methods=['POST'])
def submit():
    # Handle POST request
    data = request.form

    request.form.clear

    response = add_new_transaction(data)
    print('Paso POST')
    print(data)

    transactions = load_transactions_from_db()

    #this executes the page
    return redirect(url_for('index'))


#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
