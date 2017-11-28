"""
File: account.py
Description: File that houses everything that has to do with user validation
             and authentication for the program.
Authors: Steven Landau, Tory Leo, Talha Azhar
"""

from concurrent.futures import ThreadPoolExecutor

import business_logic.sql.db_adapter as sql


# Increase the number of workers if necessary
# (number of threads in the thread pool)
EXECUTOR = ThreadPoolExecutor(max_workers=1)

def validate(username: str, password: str) -> dict:
    """
    Validate the given username and password.

    :username:  Username the user entered
    :password:  Password the user entered

    :return: If true: {"success": True, "uuid": uuid}, if
             the username or password are invalid then
             a map with "success" set to False is returned
             along with attributes that map the name of the
             field that failed to the description of why it failed
             ex: {"username": "User does not exist"}
    """
    validation_check = {}
    
    # Check to see if the username was left blank
    if username.strip() == "":
        validation_check["success"] = False
        validation_check["username"] = "Username cannot be left blank."

    # Check to see if the username is taken
    elif not sql.is_username_taken(username):
        validation_check["success"] = False
        validation_check["username"] = "Username is incorrect"

    # Check to see if the password was left blank
    if password.strip() == "":
        validation_check["success"] = False
        validation_check["password"] = "Password cannot be left blank."


    if not validation_check.get("success", True):
        return validation_check

    else:
        return sql.verify_credentials(username, password)

def create(username: str, password: str, firstname: str, lastname: str, \
        email: str, state: str, city: str, street: str, \
        street2: str, interests: str) -> dict:
    """
    Create an account with the given credentials

    :username:  Username of the user. Cannot be left blank.
    :password:  Password associated with the user. Cannot be None.
    :firstname: First name of the user. Can be blank or None.
    :lastname:  Last name of the user. Can be blank or None.
    :email:     Email of the user. Can be blank or None.
    :state:     State the user lives in. Cannot be blank or None.
    :city:      City the user lives in. Can be blank or None.
    :street:    Street the user lives on. Can be blank or None.
    :street2:   address line 2. Can be blank or None.
    :interests: Comma seperated string of the users interests.
                Cannot be blank or None.

    :return:    If information is all valid a map with {"success": True, "uuid": uuid},
                will be returned. Otherwise a map with success set to false and attributes
                that indicate what field is missing/invalid is returned.
    """
    validation_check = {}
    if not username:
        validation_check["success"] = False
        validation_check["username"] = "Username cannot be left blank."
    elif sql.is_username_taken(username):
        validation_check["success"] = False
        validation_check["username"] = "Username is already taken"
    if not password:
        validation_check["success"] = False
        validation_check["password"] = "Password cannot be left blank"

    if not interests:
        validation_check["success"] = False
        validation_check["interests"] = "You are required to have at least one interest"

    if not validation_check.get("success", True):
        return validation_check

    interests = interests.split(',')  # Interests should be comma seperated
    registration_response = sql.register_account(username, password, firstname, lastname, \
            email, state, city, street, street2, interests)

    # If we were registered successfully
    # update the interest associations on another thread
    if registration_response['success']:
        EXECUTOR.submit(sql.update_interests, interests)

    return registration_response





