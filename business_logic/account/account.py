"""
File: login.py
Description: TODO
Authors: Steven Landau, Tory Leo, Talha Azhar
"""

import business_logic.sql.db_adapter as sql

def validate(username: str, password: str) -> dict:
    """
    TODO
    """
    if username.strip() == "":
        return {"error": "Username cannot be left blank."}
    elif password.strip() == "":
        return {"error": "Password cannot be left blank."}
    else:
        return sql.verify_credentials(username, password)

def create(username: str, password: str, firstname: str, lastname: str, \
        email: str, state: str, city: str, street: str, \
        street2: str, interests: str) -> dict:
    """
    TODO
    """
    if username is None:
        return {"success": False,
                "errors": "Username is required."}
    elif sql.is_username_taken(username):
        return {"success": False,
                "errors": "That username has already been taken."}
    elif password is None:
        return {"success": False,
                "errors": "Password is required."}
    elif interests is None:
        return  {"success": False,
                "errors": "You are required to have at least one interest"}

    return sql.register_account(username, password, firstname, lastname, \
            email, state, city, street, street2, interests)

        
