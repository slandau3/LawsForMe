import business_logic.login.login as login
import json
from flask import Flask, session, render_template, request, Response, redirect
app = Flask(__name__)
app.secret_key = "secret key"



@app.route('/')
def hello_word():
    login.validate()
    return render_template('home.html', user="steven")

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    """
    TODO
    """
    if request.method == 'POST':
        # Attempt to obtain the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # actually validate the credentials
        login_attemp = login.validate(username, password)

        if login_attemp['success']:
            return redirect("/") # TODO: Figure out where we actually want to redirect them
        else:
            # An error has occured, we need to respond to the request with details 
            # about what went wrong in json form
            return Response(json.dumps(login_attempt), mimetype='application/json; charset=utf-8')
    elif request.method == 'GET':
        pass
    else:
        raise NotImplemented()


if __name__ == '__main__':
    app.run(debug=True)
