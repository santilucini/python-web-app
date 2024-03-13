from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World, wuujuu"


#This is to excecute the app with Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
