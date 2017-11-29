"""
File: app.py
Description: Main program for the LawsForMe program. Defines a set of routes that are
             used to access and interact with the website.

Authors: Steven Landau, Tory Leo, Talha Azhar
"""

import json
import business_logic.account.account as account
import business_logic.sql.db_adapter as db


# initialize flask
from flask import Flask, session, render_template, \
                request, Response, redirect, flash
app = Flask(__name__)
app.secret_key = "secret key"


def __session_has_uuid():
    """
    Determine whether or not a session has a uuid attached
    to it.

    :return: True if it does, False otherwise
    """
    uuid = session.get('uuid', False)
    # keep in mind uuid may not be a boolean, which is why I'm comparing it to one
    # if you find a way to cast uuid to a boolean while its of type uuid then feel
    # free to change it
    return uuid != False

@app.route('/')
def home():
    """
    Render the home page of the website.
    If the user has a uuid attached to their session
    the logged in version of the home page will be loaded
    that lists out laws that may interest them.
    Otherwise the not logged in version of the page
    is loaded which contains information about the website
    and general "about us" stuff.
    """
    logged_in = __session_has_uuid()
    if logged_in:
        laws_of_interests = db.get_laws_of_interests(session['uuid'])
        return render_template('index.html',
                               logged_in=logged_in, laws_of_interests=laws_of_interests)

    return render_template('index.html', logged_in=logged_in)


@app.route('/cake/<haha>')
def get(haha):
    words = db.get_words(haha)
    return render_template('wiki.html', paragraph = words)



@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    """
    Log the user out by deleting the uuid attached to their session
    and redirect them to the home page.
    If the person is not logged in they are simply redirected to the
    home page.
    """
    uuid = session.get('uuid', False)
    if uuid:
        # user is logged in so lets get rid fo their uuid
        del session['uuid']

    return redirect('/')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    :GET: Render the "login.html" page

    :POST: Attempt to validate the information the user
           provided. If the data failed to validate
           (invalid username or password) the login page
           is rerendered with an error message at the appropriate
           field(s). If the data is valid the user's session is 
           assigned their uuid and redirected to the home page
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
            return render_template("login.html", username = login_attempt.get("username", ""), password = login_attempt.get("password", ""))

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
    :GET: Render the "createAccount.html" page

    :POST: Submit the data in the "createAccount.html" page.
           The data is verified and if an error occurs the page 
           will be rerendered with an error message on the fields
           that were invalid. If no such error occured the users
           account will be created and they will be redirected to
           the login page.
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
        if not create_account_resp['success']:
            return render_template("createAccount.html",

                                   username=create_account_resp.get("username", ""),
                                   password=create_account_resp.get("password", ""),
                                   interests=create_account_resp.get("interests", ""))
        else:
            session['uuid'] = create_account_resp.get('uuid')
            return redirect("/login/")
    else:
        raise NotImplementedError()



@app.route('/forum/', methods=['GET', 'POST'])

def load_forum_discussions():
    """
        :GET: Render the "forum.html" page

        :POST: Gets a sort request. Renders "forum.html" based on input
    """
    if request.method == 'GET':
        discussions = db.get_num_4_disc()
        return render_template('forum.html', disc=discussions, logged_in=__session_has_uuid())

    elif request.method == 'POST':
        type = request.form.get('sort')
        discussions = db.get_num_4_disc_sort(type)
        return render_template('forum.html', disc=discussions, t = type, logged_in=__session_has_uuid())





@app.route('/forum/<form_name>', methods=['GET', 'POST'])
def load_threads(form_name):
    """
        :GET: Render the "thread.html" page

        :POST: Gets a sort request. Renders "thread.html" based on input
    """
    if request.method == 'GET':
        # threads = db.get_threads(form_name)
        num_comm = db.get_num_comments(form_name)
        # return render_template('thread.html', thr = threads)
        return render_template('thread.html', com=num_comm, fn = form_name)

    elif request.method == 'POST':
        type = request.form.get('sort')
        num_comm = db.get_num_4_thread_sort(form_name, type)
        return render_template('thread.html', com=num_comm, t = type, fn = form_name, logged_in=__session_has_uuid())



def __load_comments_get(next_name):
    """
            Helper function to load comments.
        """
    thread = db.get_thread(next_name)
    comments = db.get_comments(next_name)
    # return render_template('thread.html', thr = threads)
    return render_template('comments.html', thr=thread, com=comments, nn=next_name, logged_in=__session_has_uuid())


@app.route('/forum/discussions/<next_name>', methods=['GET', 'POST'])
def load_comments(next_name):
    """
            :GET: Render the "comment.html" page

            :POST: Gets the comments and then renders "comment.html" based on input
        """
    if request.method == 'GET':
        return __load_comments_get(next_name)
    elif request.method == 'POST':
        # type = request.form.get('sort')
        if not __session_has_uuid():
            return __load_comments_get(next_name)

        user_id = session.get("uuid")
        type = request.form.get('comment')
        db.add_comments(type, next_name, user_id)
        return __load_comments_get(next_name)



@app.route('/account/', methods=['GET', 'POST'])
def load_interests():
    """
        :GET: Render the "account.html" page

        :POST: Gets a insert or delete request. Renders "account.html" based on input
    """
    if request.method == 'GET':
        if not __session_has_uuid():
            return "Please login"

        user_id = session.get("uuid")
        interests = db.get_interests(user_id)
        return render_template('account.html', i = interests, logged_in=__session_has_uuid())


    elif request.method == 'POST':
        user_id = session.get("uuid")
        int = request.form.get('daInterest')
        if int:
            db.add_interest(int, user_id)

        delInt = request.form.get('delete')
        if delInt:
            db.del_interest(delInt, user_id)
            print(delInt)

        interests = db.get_interests(user_id)
        return render_template('account.html', i=interests, logged_in=__session_has_uuid())


if __name__ == '__main__':
    app.run(debug=True)
