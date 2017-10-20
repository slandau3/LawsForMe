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
        
