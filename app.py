import business_logic.account.account as account
import json
from flask import Flask, session, render_template, request, Response, redirect
app = Flask(__name__)
app.secret_key = "secret key"



@app.route('/')
def hello_word():
    account.validate()
    return render_template('home.html', user="steven")

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    """
    TODO
    """
    if request.method == 'POST':
        # Attempt to obtain the username and password from the form
        username = request.form.get('username', False)
        password = request.form.get('password', False)

        # actually validate the credentials
        login_attempt = account.validate(username, password)

        if login_attempt['success']:
            return redirect("/") # TODO: Figure out where we actually want to redirect them
        else:
            # An error has occured, we need to respond to the request with details 
            # about what went wrong in json form
            return Response(json.dumps(login_attempt), mimetype='application/json; charset=utf-8')
    elif request.method == 'GET':
        pass
    else:
        raise NotImplemented()


@app.route('/createAccount/', methods = ['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('createAccount.html', author="Tory", name="steven")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Don't know if this is correct since state is a drop down
        state = request.form.get('state')
        city = request.form.get('city')
        street = request.form.get('street')
        street2 = request.form.get('street2')
        postal_code = request.form.get('postalCode')
        interests = request.form.get('interests')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')


        create_account_resp = account.create(username, password, \
                firstname, lastname, email, state, city, street, \
                street2, postal_code, interests)

        if create_account_resp['success']:
            return redirect("/")
        else:
            return Response(json.dumps(create_account_resp), mimetype='application/json; charset=utf-8')
    else:
        raise NotImplemented()






        pass
		
if __name__ == '__main__':
    app.run(debug=True)
