"""
File: db_adapter.py
Description: The functions in this file provide an interface between 
             the rest of the program and the databaes. This file should
             contain every function that is needed to interact with the
             database. The functions in this file do not do any 
             verification aside from constraint checks when 
             performing queries.

Authors: Steven Landau, Tory Leo, Talha Azhar
"""

# password storage
import hashlib

import psycopg2 as psql
import uuid



# TODO: Make all possible queries in this file

#
# Standard DB
#

cursor.execute("SET character_set_connection=utf8mb4;") #same as above

def __open_connections() -> tuple:
    """
    TODO

    Return:     conn and curr
    """
    conn = psql.connect(CONNECTION_INFO)
    curr = conn.cursor()
    return conn, curr
#
# SELECTS
#
def get_all_users():
    return None


#
# INSERTS
#


#
# MISC
#


def __hash_password(password: str) -> str:
    """
    TODO
    """
    m = hashlib.sha256(password.encode('utf-8'))
    return m.hexdigest()

def verify_credentials(username: str, password: str) -> bool:
    """
    Ensure that the givne account information is valid
    by comparing the username and password to those stored in the database.
    The password is NOT retrieved from the database, rather it is
    simply used in comparison in the SQL query.

    username: String that represents a users username
    password: String that represents the users password. Handle with care

    Return: Map that has a "success" attribute which indicates whether or not the credentials are correct.
            If the credentials turn out to be incorrect the map will also have a "error" attribute that
            contains a description of why the credentials may be incorrect.
    """
    conn, curr = __open_connections()

    curr.execute('SELECT 1 FROM "user" WHERE username=%s AND password=%s', (username, __hash_password(password)))
    response = curr.fetchone()

    curr.close()
    conn.close()

    if response == None:
        return {"error": "Username or password is incorrect.",
                "success": False}
    else:
        return {"success": True}

