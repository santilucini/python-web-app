from flask import Flask, render_template, jsonify

app = Flask(__name__)

TRANSACTIONS = [
    {
        'id': 1,
        'date': '01/01/1999',
        'category': 'Supermarket',
        'desc': 'Monster',
        'income': '0',
        'outcome': '1500'
    },
    {
        'id': 2,
        'date': '01/02/1999',
        'category': 'Sueldo',
        'desc': 'Work',
        'income': '10000',
        'outcome': '0'
    }
]

@app.route("/")
def hello_world():
    #this executes the page
    return render_template('home.html',transactions=TRANSACTIONS)

@app.route("/api/transactions")
def list_transactions():
    return jsonify(TRANSACTIONS)

#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
