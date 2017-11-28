"""
File: login.py
Description: TODO
Authors: Steven Landau, Tory Leo, Talha Azhar
"""

from concurrent.futures import ThreadPoolExecutor

import business_logic.sql.db_adapter as sql

EXECUTOR = ThreadPoolExecutor(max_workers=1)

def validate(username: str, password: str) -> dict:
    """
    TODO
    """
    error = {}
    if username.strip() == "":
        error["success"] = False
        error["username"] = "Username cannot be left blank."
    elif not sql.is_username_taken(username):
        error["success"] = False
        error["username"] = "Username is incorrect"

    if password.strip() == "":
        error["success"] = False
        error["password"] = "Password cannot be left blank."
    elif not sql.is_password_taken(password):
        error["success"] = False
        error["password"] = "Password is incorrect"

    if not error["success"]:
        return error

    else:
        return sql.verify_credentials(username, password)

def create(username: str, password: str, firstname: str, lastname: str, \
        email: str, state: str, city: str, street: str, \
        street2: str, interests: str) -> dict:
    """
    TODO
    """
    error = {}
    if not username:
        error["success"] = False
        error["username"] = "Username cannot be left blank."
    elif sql.is_username_taken(username):
        error["success"] = False
        error["username"] = "Username is already taken"
    if not password:
        error["success"] = False
        error["password"] = "Password cannot be left blank"

    if not interests:
        error["success"] = False
        error["interests"] = "You are required to have at least one interest"

    if not error["success"]:
        return error

    interests = interests.split(',')  # Interests should be comma seperated
    registration_response = sql.register_account(username, password, firstname, lastname, \
            email, state, city, street, street2, interests)

    if registration_response['success']:
        # If we were registered successfully
        # update the interest associations on another thread
        EXECUTOR.submit(sql.update_interests, interests)
    return registration_response





