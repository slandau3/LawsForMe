import business_logic.account.account as account
import business_logic.sql.db_adapter as db
import json

# initialize flask
from flask import Flask, session, render_template, \
                request, Response, redirect
app = Flask(__name__)
app.secret_key = "secret key"



@app.route('/')
def home():
    return render_template('index.html')

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

        print(login_attempt)

        if login_attempt['success']:
            return redirect("/") # TODO: Figure out where we actually want to redirect them
        else:
            # An error has occured, we need to respond to the request with details 
            # about what went wrong in json form
            return Response(json.dumps(login_attempt), mimetype='application/json; charset=utf-8')
    elif request.method == 'GET':
        print("Getting")
        return render_template('login.html')
    else:
        raise NotImplemented()


@app.route('/createAccount/', methods = ['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('createAccount.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Don't know if this is correct since state is a drop down
        state = request.form.get('state')
        city = request.form.get('city')
        street = request.form.get('street')
        street2 = request.form.get('street2')
        interests = request.form.get('interests')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')


        create_account_resp = account.create(username, password, \
                firstname, lastname, email, state, city, street, \
                street2, interests)
        print(create_account_resp)
        if create_account_resp['success']:
            session['uuid'] = create_account_resp.get('uuid')
            return redirect("/login/")
        else:
            print("failed")
            # TODO: make the page display the fields that caused an error
            return Response(json.dumps(create_account_resp), mimetype='application/json; charset=utf-8')
    else:
        raise NotImplemented()
		
@app.route('/forum/discussions/', methods = ['GET'])
def load_forum_discussions():
    if request.method == 'GET':
        discussions = db.getDiscussions()
        return None
        #return render_template('discussions.html', name=)

if __name__ == '__main__':
    app.run(debug=True)
