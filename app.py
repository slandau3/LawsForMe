import business_logic.login.login as login
from flask import Flask, session, render_template, request
app = Flask(__name__)
app.secret_key = "secret key"



@app.route('/')
def hello_word():
    login.validate()
    return render_template('home.html', user="steven")

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login.validate()
    elif request.method == 'GET':
        pass
    else:
        raise NotImplemented()


if __name__ == '__main__':
    app.run(debug=True)
