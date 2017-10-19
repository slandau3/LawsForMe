from app.login import *
from flask import Flask, session, render_template, request
app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def hello_word():
    return render_template('home.html', user="steven")

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        raise NotImplemented()


@app.route('/createAccount/', methods = ['GET', 'POST'])
def create_account():
		return render_template('createAccount.html', author="Tory", name="steven")
		
if __name__ == '__main__':
    app.run(debug=True)
