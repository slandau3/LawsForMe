"""
TODO
"""

import json
import business_logic.account.account as account
import business_logic.sql.db_adapter as db

# initialize flask
from flask import Flask, session, render_template, \
                request, Response, redirect
app = Flask(__name__)
app.secret_key = "secret key"


def __session_has_uuid():
    uuid = session.get('uuid', False)
    # keep in mind uuid may not be a boolean, which is why I'm comparing it to one
    # if you find a way to cast uuid to a boolean while its of type uuid then feel
    # free to change it
    return uuid != False

@app.route('/')
def home():
    logged_in = __session_has_uuid()
    if logged_in:
        # TODO: make this render more stuff such as links to the persons interests
        laws_of_interests = db.get_laws_of_interests(session['uuid'])
        return render_template('index.html', logged_in=logged_in, laws_of_interests=laws_of_interests)
    else:
        return render_template('index.html', logged_in=logged_in)



@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    uuid = session.get('uuid', False)
    if uuid:
        # user is logged in so lets get rid fo their uuid
        del session['uuid']

    return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
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
            session['uuid'] = login_attempt['uuid']
            return redirect("/") # TODO: Figure out where we actually want to redirect them
        else:
            # An error has occured, we need to respond to the request with details 
            # about what went wrong in json form
            return Response(json.dumps(login_attempt), mimetype='application/json; charset=utf-8')
    elif request.method == 'GET':
        print("Getting")
        return render_template('login.html')
    else:
        raise NotImplementedError()

@app.route('/createAccount/', methods=['GET', 'POST'])
def create_account():
    """
    TODO
    """
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
        raise NotImplementedError()

@app.route('/forum/discussions/', methods=['GET'])
def load_forum_discussions():
    if request.method == 'GET':
        discussions = db.getDiscussions()
        return None
        #return render_template('discussions.html', name=)

if __name__ == '__main__':
    app.run(debug=True)
