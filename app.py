from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import load_transactions_from_db, load_transaction_from_db, add_new_transaction, get_initial_balance, get_categories,update_transaction,load_from_db_by_category,get_last_inserted
from database import add_new_transaction_saving
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/expenses")
def index():
    try:
        transactions = load_transactions_from_db()

        initial_balance = get_initial_balance(1,"amount_arg")
        

        balance = initial_balance

        for transaction in transactions:
            if transaction['type'] == 1:
                balance -= transaction['amount_arg']
            elif transaction['type'] == 2:
                balance += transaction['amount_arg']

            transaction['balance'] = balance

        transactions.reverse()
        #this executes the page
        #return jsonify(transactions)
        return render_template('base.html',page='expenses.html',transactions=transactions,balance=balance, initial_balance=initial_balance)
    except Exception as e:
        return e

@app.route("/savings")
def savings():
    try:
        transactions = load_from_db_by_category(3)

        initial_balance = get_initial_balance(23,'amount_usd')

        balance = initial_balance

        for transaction in transactions:
            if transaction['type'] == 1:
                balance -= transaction['amount_usd']
            elif transaction['type'] == 2:
                balance += transaction['amount_usd']

            transaction['balance'] = balance

        transactions.reverse()
        #this executes the page
        #return jsonify(transactions)
        #return render_template('base.html',page='expenses.html',transactions=transactions,balance=balance, initial_balance=initial_balance)
        return render_template('base.html',page='table_template.html',transactions=transactions,balance=balance,initial_balance=initial_balance)
    except Exception as e:
        return e

@app.route("/debts")
def debts():
    try:
        return render_template('base.html',page='debts.html')
    except Exception as e:
        return e

@app.route("/dashboard")
def dashboard():
    """
    fig, ax = plt.subplots()
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 4, 9, 16]
    ax.plot(x, y)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #return render_template('index.html', plot_url=plot_url)
    """
    try:
        return render_template('base.html',page='dashboard.html', 
                               #plot_url=plot_url
                               )
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
    return render_template('base.html',page='new_transaction.html',categories=categories,today=today)

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
    
    
    if data['Category'] == '3':
        last_id = get_last_inserted()
        savings_data = {
            "id_transaction": last_id,
            "amount": data['Amount_USD']
        }       

        add_new_transaction_saving(savings_data)
    
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
