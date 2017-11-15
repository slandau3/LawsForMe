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
        return {"success": False, "error": "Username cannot be left blank."}
    elif password.strip() == "":
        return {"success": False, "error": "Password cannot be left blank."}
    else:
        return sql.verify_credentials(username, password)

def create(username: str, password: str, firstname: str, lastname: str, \
        email: str, state: str, city: str, street: str, \
        street2: str, interests: str) -> dict:
    """
    TODO
    """
    if not username:
        return {"success": False,
                "errors": "Username is required."}
    elif sql.is_username_taken(username):
        return {"success": False,
                "errors": "That username has already been taken."}
    elif not password:
        return {"success": False,
                "errors": "Password is required."}
    elif not interests:
        return  {"success": False,
                "errors": "You are required to have at least one interest"}

    return sql.register_account(username, password, firstname, lastname, \
            email, state, city, street, street2, interests)

        
