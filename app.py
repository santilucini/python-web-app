from flask import Flask, render_template, jsonify
from database import load_transactions_from_db, load_transaction_from_db

app = Flask(__name__)

@app.route("/")
def hello_world():
    transactions = load_transactions_from_db()

    #this executes the page
    return render_template('home.html',transactions=transactions)

@app.route("/api/transactions")
def list_transactions():
    transactions = load_transactions_from_db()
    return jsonify(transactions)

@app.route("/transaction/<id>")
def show_transact(id):
    transact = load_transaction_from_db(id)
    return jsonify(transact)

#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
